import socket
import json

HOST = 'pub-vrs.adsbexchange.com'
PORT = 32005
#Website: https://www.adsbexchange.com/data/

class StreamSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect((self.host, self.port))


class AircraftStream(StreamSocket):
    """
        Note: Strong assumptions about the format of the return data
    """
    def stream_data(self):
        data = b''
        while True:
            data = data + self.client.recv(4096)
            data, vals = self.stream_parser(data)
            yield vals
            self.segment_parser(vals)


    def stream_parser(self, response_segment):
        """
            Removes excess segments from stream_segment before calling a segment parser
        """
        previous_val = None
        #Remove append
        try:
            previous_val, response_segment = response_segment.split(b']}')
        except ValueError as e:
            pass
        #Remove prepend
        try:
            _, response_segment = response_segment.split(b'{"acList":[')
        except ValueError as e:
            pass

        if previous_val:
            return previous_val,response_segment
        else:
            return None, response_segment
    def segment_parser(self, segment):
        """
            Parses segments separated by commas
        """

        aircraft_datas = segment.split(b',')

        self.process_aircraft(aircraft_datas)
    def process_aircraft(self, aircraft_datas):
        for aircraft_data in aircraft_datas:
            print(aircraft_data)
            print(json.loads(aircraft_data))

k = AircraftStream(HOST,PORT)
k.connect()
k.stream_data()




