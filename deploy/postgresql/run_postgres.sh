#!/bin/bash

sudo docker run --name postgresserver \
	-e POSTGRES_PASSWORD=somestrongdbpassword \
	-v qua-pgdata:/var/lib/postgresql/data \
	-p 5432:5432 \
	-d qua-postgres:latest
