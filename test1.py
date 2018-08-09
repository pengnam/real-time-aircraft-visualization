from kafka import KafkaConsumer
consumer  = KafkaConsumer('test')
for i,msg in enumerate(consumer):
    print(i)
    print(msg)
