#! /bin/bash

source $MEDIACRITY_CONFIG

docker rm -f mediacrity-dev

docker pull mediacrity/mediacrity

mkdir -p $MEDIACRITY_DB_DATA_DIR

sudo chown 9999:9999 $MEDIACRITY_DB_DATA_DIR

docker run -d \
  --name mediacrity-dev \
  -v $MEDIACRITY_CONFIG_DIR:/mediacrity/config \
  -v $MEDIACRITY_DB_DATA_DIR:/mediacrity/data/postgres \
  -v $MEDIACRITY_MESSAGE_DATA_DIR:/mediacrity/data/rabbit \
  -p $MEDIACRITY_MESSAGE_ADMIN_PORT:15672 \
  -p $MEDIACRITY_WEB_PORT:8000 \
  -e MEDIACRITY_DEV_CONTAINER=true \
  -e MEDIACRITY_CONFIG=/mediacrity/config/mediacrity-settings.sh \
  mediacrity/mediacrity
