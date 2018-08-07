from kafka import KafkaProducer, KafkaClient
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
        self.producer = self.KafkaProducer(boostrap_server=host)
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



