from kafka import KafkaProducer
import logging
logging.basicConfig(level=logging.DEBUG)

producer = KafkaProducer(bootstrap_servers='0.0.0.0:9092')

for _ in range(100):
    result = producer.send("test",b"this is great")

