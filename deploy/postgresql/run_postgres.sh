#!/bin/bash

sudo docker run --name postgres01 \
	-e POSTGRES_PASSWORD=somestrongdbpassword \
	-v pgdata:/var/lib/postgresql/data \
	-p 5432:5432 \
	-d qua-postgres:latest
