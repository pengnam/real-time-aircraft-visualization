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
            data = self.stream_parser(data)
            data = self.segment_parser(data)


    def stream_parser(self, response_segment):
        """
            Removes excess segments from stream_segment before calling a segment parser
            Strips:
                1) {"aclist":[
                2)]}
            Returns bytes of aircrafts separated by a ','. Note that there might be trailing excess bytes
        """
        response_segment = response_segment.replace(b']}', b',')
        response_segment = response_segment.replace(b'{"acList":[', b'')
        return response_segment

    def segment_parser(self, segment):
        """
            Parses segments into sections
            Returns generator object
        """

        try:
            while True:
                start_index = segment.index(b'{')
                split_index = segment.index(b'},{')
                print(start_index, split_index)
                aircraft_data = segment[start_index:split_index+1]
                self.process_aircraft(aircraft_data)
                segment = segment[split_index+2:]
        except ValueError as e:
            print("end")
            return segment

    def process_aircraft(self, aircraft_data):
        print(json.loads(aircraft_data))

k = AircraftStream(HOST,PORT)
k.connect()
k.stream_data()




