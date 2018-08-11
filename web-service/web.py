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

"""
class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value" : value}
        data = json.dumps(data)

    @web.asynchronous
    def post(self):
        pass
"""
app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
#    (r'/api', ApiHandler)
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
