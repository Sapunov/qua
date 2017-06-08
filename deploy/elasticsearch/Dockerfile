FROM docker.elastic.co/elasticsearch/elasticsearch:5.2.2

USER root

COPY conf/* /usr/share/elasticsearch/config/
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/config/* \
	&& export "ES_JAVA_OPTS=-Xms1g -Xmx1g"

USER elasticsearch
