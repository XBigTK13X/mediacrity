#! /bin/bash

source $MEDIACRITY_CONFIG

docker rm -f mediacrity-dev

sudo rm -rf $MEDIACRITY_DB_DATA_DIR

if [ ! -z $1 ]; then
  script/docker/dev-start.sh
  sleep 5s
  script/db/migrate.sh
fi
