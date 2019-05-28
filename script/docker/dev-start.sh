#! /bin/bash

source $MEDIACRITY_CONFIG

CREATE_DB=$1

docker rm -f mediacrity-dev

docker pull mediacrity/mediacrity

mkdir -p $MEDIACRITY_DB_DATA_DIR

sudo chown 101:103 $MEDIACRITY_DB_DATA_DIR

mkdir -p $MEDIACRITY_MESSAGE_DATA_DIR

docker run -d \
  --name mediacrity-dev \
  -v $MEDIACRITY_CONFIG_DIR:/mediacrity/config \
  -v $MEDIACRITY_DB_DATA_DIR:/mediacrity/data/postgres \
  -v $MEDIACRITY_MESSAGE_DATA_DIR:/mediacrity/data/rabbit \
  -v $MEDIACRITY_MEDIA_DIR:/mediacrity/media \
  -p $MEDIACRITY_DB_PORT:5432 \
  -p $MEDIACRITY_MESSAGE_PORT:5672 \
  -p $MEDIACRITY_MESSAGE_ADMIN_PORT:15672 \
  -p $MEDIACRITY_CONTENT_SERVER_PORT:80 \
  -e MEDIACRITY_DEV_CONTAINER=true \
  -e MEDIACRITY_CONFIG=/mediacrity/config/mediacrity-settings.sh \
  mediacrity/mediacrity

if [ ! -z $CREATE_DB ]; then
  echo "Wait for postgres to start, then ensure user/db is created"
  sleep 5

  docker exec -it mediacrity-dev su postgres -c "createuser $MEDIACRITY_DB_USER"
  docker exec -it mediacrity-dev su postgres -c "createdb $MEDIACRITY_DB_USER"
fi
