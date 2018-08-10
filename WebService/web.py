from tornado import websocket, web, ioloop
from pipeline import DataPipelineConsumer
import json


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("OPENING")
        consumer = DataPipelineConsumer("aircraft", "aircraft.avsc")
        msgs = consumer.read()
        for msg in msgs:
            self.write_message(msg)


    def on_close(self):
        print("Socket closing")
