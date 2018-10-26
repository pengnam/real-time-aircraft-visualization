# Gandalf
## Brief Description
This application is solely composed of microservices: a kafka service, a streaming service, a web service and a client service.
I really wanted to try the following ideas:
1. WebSockets
2. Apache Kafka - a distributed streaming platform (https://kafka.apache.org/)
3. Apache Avro - a data serializer (http://avro.apache.org/)
4. deck.gl - large-scale WebGL-powered (GPU powered) data visualization (http://deck.gl/)
5. React.js

I needed practice with some others:
1. Building microservices
2. Using Docker
3. Programming in python/javascript

The application streams data from https://public-api.adsbexchange.com/ . (Thank you ADS-B Exchange)
The data gives a stream of aircraft positions updated every 5s. The application was able to handle the throughput of data.

![Alt text](screenshot.png)

Picture: Visualization after about 30s of aircraft plotting
