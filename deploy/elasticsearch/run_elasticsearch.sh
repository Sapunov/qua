#!/bin/bash

sudo docker run --name esserver \
	-v esdata:/usr/share/elasticsearch/data \
	-v esconfig:/usr/share/elasticsearch/config \
	-d qua-elasticsearch
