#! /bin/bash

source $MEDIACRITY_CONFIG

docker rm -f mediacrity-db

docker pull postgres

docker run -d \
  --name mediacrity-db \
  -e POSTGRES_USER=$MEDIACRITY_DB_USER \
  -e POSTGRES_PASSWORD=$MEDIACRITY_DB_PASSWORD \
  -e POSTGRES_DB=$MEDIACRITY_DB_NAME \
  -p 5432:5432 \
  -v $MEDIACRITY_DB_DATA_DIR:/var/lib/postgresql/data \
  -d postgres

  docker rm -f mediacrity-queue

  docker pull rabbitmq:3-management

  docker run -d \
    --hostname mediacrity-queue \
    --name mediacrity-queue \
    -p 5672:5672 \
    -p 15672:15672 \
    -v $MEDIACRITY_QUEUE_DATA_DIR:/var/lib/rabbitmq \
    rabbitmq:3-management
