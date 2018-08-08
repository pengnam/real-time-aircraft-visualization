FROM openjdk:8u171-jre-alpine

ARG kafka_version=1.0.0
ARG scala_version=2.11
ARG glibc_version=2.27-r0


ENV KAFKA_VERSION=$kafka_version \
    SCALA_VERSION=$scala_version \
    KAFKA_HOME=/opt/kafka_${scala_version}-${kafka_version}\
    GLIBC_VERSION=$glibc_version

ENV PATH=${PATH}:${KAFKA_HOME}/bin

COPY start-kafka.sh /usr/bin 
COPY download-kafka.sh /tmp/

RUN dos2unix /usr/bin/start-kafka.sh

RUN apk add --no-cache curl jq docker \
 && mkdir /opt \
 && chmod a+x /usr/bin/start-kafka.sh \
 && chmod a+x /tmp/download-kafka.sh \
 && ls /tmp/ \
 && sync && /tmp/download-kafka.sh \
 && tar xfz /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C /opt \
 && rm /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
 && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-${GLIBC_VERSION}.apk \
 && apk add --no-cache --allow-untrusted glibc-${GLIBC_VERSION}.apk \
 && rm glibc-${GLIBC_VERSION}.apk
  
CMD ["start-kafka.sh"]

