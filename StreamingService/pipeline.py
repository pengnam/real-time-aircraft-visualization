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

