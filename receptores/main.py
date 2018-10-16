import kivy
from kivy import platform
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from components.listview import MenuListView
import tpv_websocket.receptor as receptor
import os
import threading

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
            font_size: "20dp"
            text: root.texto
        ButtonIcon:
            size_hint:  .3, 1
            icon: res.FA_TRASH
            on_release: root.borrar_linea()

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
            row_height: dp(40)
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
    def __init__(self, **args):
        super(ReceptorWidget, self).__init__(**args)

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
        if platform == "android":
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load('beep-06.wav')
            if sound:
                sound.play()
        elif platform == "linux":
            os.system("aplay beep-06.wav")
            os.system("aplay beep-06.wav")
            os.system("aplay beep-06.wav")

        elif platform == "macosx":
            os.system("afplay beep-06.wav")
            os.system("afplay beep-06.wav")
            os.system("afplay beep-06.wav")

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

        if platform == "android":
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load('beep-06.wav')
            if sound:
                sound.play()
        elif platform == "linux":
            os.system("aplay beep-06.wav")
            os.system("aplay beep-06.wav")
            os.system("aplay beep-06.wav")

        elif platform == "macosx":
            os.system("afplay beep-06.wav")
            os.system("afplay beep-06.wav")
            os.system("afplay beep-06.wav")


class ReceptorApp(App):
    def build(self):
        self.receptor = ReceptorWidget()
        self.hilo = threading.Thread(target=receptor.run_websoker,
                                args=("ws://localhost:8000/ws/impresion/caja/",self.receptor))
        self.hilo.start()
        return self.receptor




if __name__ == '__main__':
    ReceptorApp().run()
