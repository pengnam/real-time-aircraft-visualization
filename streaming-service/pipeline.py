from kafka import KafkaProducer, KafkaConsumer
import avro.schema
import io
import avro.io
from avro.io import DatumWriter, DatumReader

class DataPipeline:
    def __init__(self, topic, schema_path):
        self.topic = topic
        self.schema = avro.schema.Parse(open(schema_path).read())
        self.keys = [field.name for field in self.schema.fields]


class DataPipelineProducer(DataPipeline):
    def __init__(self,  *args,host='localhost:9092', **kwargs):
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
        print(data)
        self.producer.send(self.topic, raw_bytes)

class DataPipelineConsumer(DataPipeline):
    def __init__(self, *args, host='localhost:9092', **kwargs):
        self.consumer= KafkaConsumer(auto_offset_reset='latest', consumer_timeout_ms=1000, bootstrap_servers=host)
        super().__init__(*args, **kwargs)

    def read(self):
        self.consumer.subscribe([self.topic])
        while True:
            for msg in self.consumer:
                bytes_reader = io.BytesIO(msg.value)
                decoder=avro.io.BinaryDecoder(bytes_reader)
                reader  = DatumReader(self.schema)
                value = reader.read(decoder)
                print(value)



if __name__ == "__main__":
    """
    print("INSIDE")

    cons = DataPipelineConsumer("aircraft", "aircraft.avsc")
    cons.read()
    """
