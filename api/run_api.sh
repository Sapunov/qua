#!/bin/bash

sudo docker run -d \
    --name qua-api \
    --link postgres01:postgres01
    -v qua-api-data:/var/lib/qua/data \
    -p 9000:80 \
    qua-api:latest
