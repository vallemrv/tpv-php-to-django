# @Author: Manuel Rodriguez <valle>
# @Date:   11-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 06-Jul-2018
# @License: Apache license vesion 2.0


import websocket
import json
import time

def on_message(ws, message):
    from tpv.impresora import DocPrint
    message = json.loads(message)["message"]
    doc = DocPrint("192.168.1.8")
    op = message["op"]
    if op == "open":
        doc.abrir_cajon()
    elif op == "desglose":
        doc.printDesglose(message["fecha"], message["lineas"])
    elif op == "ticket":
        cambio = float(message['efectivo']) - float(message['total'])
        doc.imprimirTicket(message['num'], message['camarero'], message['fecha'], message["mesa"],
                           message['total'], message['efectivo'], cambio, message['lineas'])
    elif op == "pedido":
        doc.imprimirPedido(message["camarero"], message["mesa"], message["hora"], message["lineas"] )
    elif op == "urgente":
        doc.imprimirUrgente(message["camarero"], message["mesa"], message["hora"], message["lineas"] )

    elif op == "preticket":
        doc.imprimirPreTicket(message["camarero"], message['numcopias'], message['fecha'],
                              message["mesa"], message['lineas'], message['total'])


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    pass


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://gsfm.mibtres.com/ws/impresion/caja/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open



    while True:
        ws.run_forever()
        time.sleep(2)
