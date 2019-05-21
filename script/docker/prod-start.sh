#! /bin/bash

source $MEDIACRITY_CONFIG

docker network rm mediacrity

docker network create mediacrity

docker rm -f mediacrity-db

docker pull postgres

docker run -d \
  --network mediacrity \
  --name mediacrity-db \
  --hostname db \
  -e POSTGRES_USER=$MEDIACRITY_DB_USER \
  -e POSTGRES_PASSWORD=$MEDIACRITY_DB_PASSWORD \
  -e POSTGRES_DB=$MEDIACRITY_DB_NAME \
  -p $MEDIACRITY_DB_PORT:5432 \
  -v $MEDIACRITY_DB_DATA_DIR:/var/lib/postgresql/data \
  -d postgres

docker rm -f mediacrity-queue

docker pull rabbitmq:3-management

docker run -d \
  --network mediacrity \
  --hostname queue \
  --name mediacrity-queue \
  -p $MEDIACRITY_MESSAGE_PORT:5672 \
  -p $MEDIACRITY_MESSAGE_ADMIN_PORT:15672 \
  -v $MEDIACRITY_MESSAGE_DATA_DIR:/var/lib/rabbitmq \
  rabbitmq:3-management

docker rm -f mediacrity-web

docker rm -f mediacrity-worker

docker pull mediacrity/mediacrity

docker run -d \
  --network mediacrity \
  --name mediacrity-web \
  --hostname web
  -p $MEDIACRITY_WEB_PORT:$MEDIACRITY_WEB_PORT \
  mediacrity/mediacrity

docker run -d \
  --network mediacrity \
  --name mediacrity-worker \
  --hostname worker
  -e MEDIACRITY_RUN_MODE="worker" \
  mediacrity/mediacrity
