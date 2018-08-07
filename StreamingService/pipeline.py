from kafka import KafkaProducer, KafkaClient
import avro.schema
import io
from avro.io import DatumWriter


class DataPipeline:
    def __init__(self, topic, schema_path, host='localhost:9092'):
        #self.producer = KafkaProducer(bootstrap_servers=host)
        self.topic = topic

        self.schema = avro.schema.Parse(open(schema_path).read())
        self.keys = [field.name for field in self.schema.fields]



    def write(self, data):
        print(data)
        store_data = {}
        for key in self.keys:
            if key in data:
                store_data[key] = data[key]
            else:
                store_data[key] = None
        writer = DatumWriter(self.schema)
        bytes_writer = io.BytesIO()
        encoder=avro.io.BinaryEncoder(bytes_writer)

        writer.write(store_data, encoder)
        raw_bytes = bytes_writer.getvalue()
        print(raw_bytes)



