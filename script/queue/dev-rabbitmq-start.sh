#! /bin/bash

source $MEDIACRITY_CONFIG

docker rm -f mediacrity-queue

docker pull rabbitmq:3-management

docker run -d \
  --hostname mediacrity-queue \
  --name mediacrity-queue \
  -p 5672:5672 \
  -p 15672:15672 \
  -v $MEDIACRITY_QUEUE_DATA_DIR:/var/lib/rabbitmq \
  rabbitmq:3-management
