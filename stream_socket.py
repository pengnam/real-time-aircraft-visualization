import socket
import json

HOST = 'pub-vrs.adsbexchange.com'
PORT = 32030

class StreamSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect((self.host, self.port))


