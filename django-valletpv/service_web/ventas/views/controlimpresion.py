# @Author: Manuel Rodriguez <valle>
# @Date:   27-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 29-Jun-2018
# @License: Apache license vesion 2.0

import websocket
import json
from datetime import datetime
from django.db.models import Q, Count, Sum, F
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site
from tokenapi.http import JsonResponse
from gestion.models import (Pedidos, Lineaspedido, Ticket, Infmesa, Teclas,
                            Ticketlineas, Receptores, Mesasabiertas, Camareros)


def imprimir_pedido(request, id):
    pedido = Pedidos.objects.get(pk=id)
    camareo = Camareros.objects.get(pk=pedido.camarero_id)
    mesa = pedido.infmesa.mesasabiertas_set.get().mesa
    lineas = pedido.lineaspedido_set.values("idart",
                                           "nombre",
                                           "precio",
                                           "pedido_id").annotate(can=Count('idart'))
    receptores = {}
    for l in lineas:
        receptor = Teclas.objects.get(id=l['idart']).familia.receptor
        if receptor.nombre not in receptores:
            receptores[receptor.nombre] = {
                "op": "pedido",
                "hora": pedido.hora,
                "receptor": receptor.nomimp,
                "camarero": camareo.nombre + " " + camareo.apellidos,
                "mesa": mesa.nombre,
                "lineas": []
            }
        l["precio"] = float(l["precio"])
        receptores[receptor.nombre]['lineas'].append(l)

    send_pedidos_ws(request, receptores)
    return JsonResponse({})

def preimprimir_pedido(request, id):
    print(id)
    return JsonResponse({})

def preimprimir_ticket(request, id):
    mesa = Mesasabiertas.objects.get(mesa_id=id)
    infmesa = mesa.infmesa
    infmesa.numcopias = infmesa.numcopias + 1
    infmesa.save()
    camareo = infmesa.camarero
    mesa = mesa.mesa
    lineas = infmesa.lineaspedido_set.filter(Q(estado="P") |
                                            Q(estado="N")).values("idart",
                                                                  "precio").annotate(can=Count('idart'),
                                                                                     totallinea=Sum("precio"))
    lineas_ticket = []
    for l in lineas:
        try:
            art = Teclas.objects.get(id=l["idart"])
            l["nombre"] = art.nombre
        except:
            art = infmesa.lineaspedido_set.filter(idart=l["idart"])
            l["nombre"] = art.nombre
        lineas_ticket.append(l)
    obj = {
        "op": "preticket",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "receptor": Receptores.objects.get(nombre='Ticket').nomimp,
        "camarero": camareo.nombre + " " + camareo.apellidos,
        "mesa": mesa.nombre,
        "numcopias": infmesa.numcopias,
        "lineas": lineas_ticket,
        'total': infmesa.lineaspedido_set.all().aggregate(Total=Sum("precio"))['Total']
    }

    send_ticket_ws(request, obj)
    return JsonResponse({})

def imprimir_ticket(request, id):
    ticket = Ticket.objects.get(pk=id)
    camarero = Camareros.objects.get(pk=ticket.camarero_id)
    lineas = ticket.ticketlineas_set.all().annotate(idart=F("linea__idart"),
                                                    precio=F("linea__precio"))

    lineas = lineas.values("idart",
                           "precio").annotate(can=Count('idart'),
                                              totallinea=Sum("precio"))
    lineas_ticket = []
    for l in lineas:
        try:
            art = Teclas.objects.get(id=l["idart"])
            l["nombre"] = art.nombre
        except:
            art = ticket.ticketlineas_set.filter(linea__idart=l["idart"])
            l["nombre"] = art.nombre
        lineas_ticket.append(l)

    obj = {
        "op": "ticket",
        "fecha": ticket.fecha + " " + ticket.hora,
        "receptor": Receptores.objects.get(nombre='Ticket').nomimp,
        "camarero": camarero.nombre + " " + camarero.apellidos,
        "mesa": ticket.mesa,
        "lineas": lineas_ticket,
        "num": ticket.id,
        "efectivo": ticket.entrega,
        'total': ticket.ticketlineas_set.all().aggregate(Total=Sum("linea__precio"))['Total']
    }
    send_ticket_ws(request, obj)
    return JsonResponse({})

def reenviarlinea(request, id, idl, nombre):
    import urllib.parse
    nombre = urllib.parse.unquote(nombre).replace("+", " ")
    pedido = Pedidos.objects.get(pk=id)
    camareo = Camareros.objects.get(pk=pedido.camarero_id)
    mesa = pedido.infmesa.mesasabiertas_set.get().mesa
    lineas = pedido.lineaspedido_set.filter(idart=idl, nombre=nombre).values("idart",
                                           "nombre",
                                           "precio",
                                           "pedido_id").annotate(can=Count('idart'))
    receptores = {}
    for l in lineas:
        receptor = Teclas.objects.get(id=l['idart']).familia.receptor
        if receptor.nombre not in receptores:
            receptores[receptor.nombre] = {
                "op": "urgente",
                "hora": pedido.hora,
                "receptor": receptor.nomimp,
                "camarero": camareo.nombre + " " + camareo.apellidos,
                "mesa": mesa.nombre,
                "lineas": []
            }
        l["precio"] = float(l["precio"])
        receptores[receptor.nombre]['lineas'].append(l)

    send_pedidos_ws(request, receptores)
    return JsonResponse({})

def abrircajon(request):
    obj = {
        "op": "open",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "receptor": Receptores.objects.get(nombre='Ticket').nomimp,
    }
    send_ticket_ws(request, obj)
    return JsonResponse({})


def send_pedidos_ws(request, datos):
    for k, v in datos.items():
        url = ''.join(['ws://', get_current_site(request).domain, '/ws/impresion/', v["receptor"], "/"])
        websocket.enableTrace(True)
        ws = websocket.create_connection(url)
        ws.send(json.dumps({"message": v}))
        ws.close()

def send_ticket_ws(request, v):
    url = ''.join(['ws://', get_current_site(request).domain, '/ws/impresion/', v["receptor"], "/"])
    websocket.enableTrace(True)
    ws = websocket.create_connection(url)
    ws.send(json.dumps({"message": v}, cls=DjangoJSONEncoder))
    ws.close()
