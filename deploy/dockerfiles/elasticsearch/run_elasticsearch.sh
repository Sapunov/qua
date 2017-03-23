#!/bin/bash

sudo docker run --name elasticsearch01 \
	-v esdata:/usr/share/elasticsearch/data \
	-v esconfig:/usr/share/elasticsearch/config \
	-d qua-elasticsearch
