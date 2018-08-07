from kafka import KafkaProducer, KafkaConsumer
import avro.schema
import io
from avro.io import DatumWriter


class DataPipeline:
    def __init__(self, topic, schema_path):
        self.topic = topic
        self.schema = avro.schema.Parse(open(schema_path).read())
        self.keys = [field.name for field in self.schema.fields]


class DataPipelineProducer(DataPipeline):
    def __init__(self, host='localhost:9092', *args, **kwargs):
        self.producer = KafkaProducer(bootstrap_servers=host)
        super().__init__(*args, **kwargs)

    def write(self, data):
        #Parsing data to select only keys in schema
        store_data = {}
        for key in self.keys:
            if key in data:
                store_data[key] = data[key]
            else:
                store_data[key] = None

        #Serialize data using AVRO
        writer = DatumWriter(self.schema)
        bytes_writer = io.BytesIO()
        encoder=avro.io.BinaryEncoder(bytes_writer)

        writer.write(store_data, encoder)
        raw_bytes = bytes_writer.getvalue()

        #Place into pipeline
        self.producer.send(self.topic, raw_bytes)

class DataPipelineConsumer(DataPipeline):
    def __init__(self, host='localhost:9092', *args, **kwargs):
        self.consumer= KafkaConsumer(auto_offset_reset='earliest', consumer_timeout_ms=1000, bootstrap_servers=host)
        super().__init__(*args, **kwargs)

    def read(self):
        self.consumer.subscribe([self.topic])
        while True:
            for message in self.consumer:
                print(message)


if __name__ == "__main__":
    print("INSIDE")

    cons = DataPipelineConsumer("aircraft", "aircraft.avsc")
    cons.read()

