import kivy
from kivy import platform
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from components.listview import MenuListView
from tpv_websocket import ReceptorManager
import os
import json


Builder.load_string('''
#:import ButtonColor components.buttons.ButtonColor
#:import ButtonIcon components.buttons.ButtonIcon
#:import LabelColor components.labels.LabelColor
#:import res components.resources
<LineasWidget>:
    texto: ""
    BoxLayout:
        orientation: "horizontal"
        LabelColor:
            font_size: "25dp"
            text: root.texto


<PedidoWidget>:
    lista: _lista
    informacion: "Camarero Y mesa"
    canvas:
        Color:
            rgb: .7,1,.7
        Rectangle:
            size: self.size
            pos: self.pos
    anchor_x: "center"
    anchor_y: "center"
    size_hint: 1, 1
    BoxLayout:
        size_hint: 1, 1
        orientation: "vertical"
        LabelColor:
            font_size:  "20dp"
            bg_color: "#005500"
            size_hint: 1, .12
            text: root.informacion
        MenuListView:
            row_height: dp(70)
            size_hint: 1, .76
            id: _lista
        ButtonColor:
            size_hint: 1, .12
            text: "Servido"
            on_release: root.borrar_pedido()

<ReceptorWidget>:
    content: __content
    canvas:
        Color:
            rgb: 1,1,1
        Rectangle:
            size: self.size
            pos: self.pos
    anchor_x: "center"
    anchor_y: "center"
    ScrollView:
        size_hint: 1, 1
        GridLayout:
            rows: 1
            spacing: 5
            size_hint: None, 1
            width: len(self.children) * dp(300)
            id: __content


''')

class LineasWidget(AnchorLayout):
    controller = ObjectProperty()
    def borrar_linea(self):
        self.controller.lista.rm_linea(self)


class PedidoWidget(AnchorLayout):
    lista = ObjectProperty()
    controller = ObjectProperty()

    def borrar_pedido(self):
        self.controller.content.remove_widget(self)


class ReceptorWidget(AnchorLayout):
    receptor = ObjectProperty()
    mensage = StringProperty()

    def __init__(self, **args):
        super(ReceptorWidget, self).__init__(**args)


    def onMessage(self, v, st):
        if v != "":
            message = json.loads(v)["message"]
            op = message["op"]
            if op == "pedido":
                self.pedido(message["camarero"], message["mesa"], message["hora"], message["lineas"])
            elif op == "urgente":
                self.urgente(message["camarero"], message["mesa"], message["hora"], message["lineas"])


    def pedido(self, camarero, mesa, hora, lineas):
        pedido = PedidoWidget()
        pedido.controller = self
        pedido.informacion = "{0} \n  {1}  {2}".format(camarero, mesa, hora)
        for linea in lineas:
            lw = LineasWidget()
            lw.texto = "{0: >3}  {1}".format(linea["can"], linea["nombre"])
            lw.controller = pedido
            pedido.lista.add_linea(lw)
        self.content.add_widget(pedido)
        Clock.schedule_once(self.beep, 0.1)


    def urgente(self, camarero, mesa, hora, lineas):
        pedido = PedidoWidget()
        pedido.controller = self
        pedido.informacion = "URGENTE {0} \n  {1}  {2}".format(camarero, mesa, hora)
        for linea in lineas:
            lw = LineasWidget()
            lw.texto = "{0: >3}  {1}".format(linea["can"], linea["nombre"])
            lw.controller = pedido
            pedido.lista.add_linea(lw)
        self.content.add_widget(pedido)
        Clock.schedule_once(self.beep, 0.1)


    def beep(self, st):
        path_sound = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beep-06-03.wav')
        if platform == "android":
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load(path_sound)
            if sound:
                sound.play()

        elif platform == "linux":
            os.system("aplay "+ path_sound)

        elif platform == "macosx":
            os.system("afplay "+ path_sound)


class ReceptorApp(App):
    def build(self):
        self.receptor_widget = ReceptorWidget()
        self.manager = ReceptorManager("ws://localhost/ws/impresion/caja/",
                                        self.receptor_widget)
        return self.receptor_widget

    def on_pause(self):
        return True

    def on_stop(self):
        self.manager.closed = True


if __name__ == '__main__':
    ReceptorApp().run()
