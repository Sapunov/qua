#!/bin/bash

PASSWORD=$(cat password)


sudo docker run --name postgres01 \
	-e POSTGRES_PASSWORD=$PASSWORD \
	-v pgdata:/var/lib/postgresql/data \
	-d qua-postgres:latest
