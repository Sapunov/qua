#!/bin/bash

sudo docker run --name redisserver \
	-p 6379:6379 \
	-d qua-redis
