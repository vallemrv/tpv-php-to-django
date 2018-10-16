# @Author: Manuel Rodriguez <valle>
# @Date:   11-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 06-Jul-2018
# @License: Apache license vesion 2.0


import websocket
import json
import time
import threading

class receptor_manager():

    def __init__(self, controller):
        self.controller = controller

    def on_message(ws, message):
        message = json.loads(message)["message"]
        op = message["op"]
        if op == "pedido":
            ws.controller.pedido(message["camarero"], message["mesa"], message["hora"], message["lineas"])
        elif op == "urgente":
            ws.controller.urgente(message["camarero"], message["mesa"], message["hora"], message["lineas"])


    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        pass


def run_websoker(url, controller):

    websocket.enableTrace(True)
    manager = receptor_manager(controller)

    ws = websocket.WebSocketApp(url,
                                on_message = manager.on_message,
                                on_error = manager.on_error,
                                on_close = manager.on_close)
    ws.doc = manager
    ws.on_open = manager.on_open

    while True:
        ws.run_forever()
        time.sleep(2)
