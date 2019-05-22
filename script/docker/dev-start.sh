#! /bin/bash

source $MEDIACRITY_CONFIG

docker rm -f mediacrity-content

docker pull nginx

docker run -d \
  --name mediacrity-content \
  -p $MEDIACRITY_CONTENT_SERVER_PORT:80 \
  -v $MEDIACRITY_ASSET_DIR:/mediacrity/asset \
  -v $MEDIACRITY_MEDIA_DIR:/mediacrity/media \
  -v $(pwd)/script/docker/nginx.conf:/etc/nginx/nginx.conf \
  nginx

exit 0

docker rm -f mediacrity-db

docker pull postgres

docker run -d \
  --name mediacrity-db \
  -e POSTGRES_USER=$MEDIACRITY_DB_USER \
  -e POSTGRES_PASSWORD=$MEDIACRITY_DB_PASSWORD \
  -e POSTGRES_DB=$MEDIACRITY_DB_NAME \
  -p $MEDIACRITY_DB_PORT:5432 \
  -v $MEDIACRITY_DB_DATA_DIR:/var/lib/postgresql/data \
  -d postgres

docker rm -f mediacrity-queue

docker pull rabbitmq:3-management

docker run -d \
  --hostname mediacrity-queue \
  --name mediacrity-queue \
  -p $MEDIACRITY_MESSAGE_PORT:5672 \
  -p $MEDIACRITY_MESSAGE_ADMIN_PORT:15672 \
  -v $MEDIACRITY_MESSAGE_DATA_DIR:/var/lib/rabbitmq \
  rabbitmq:3-management
