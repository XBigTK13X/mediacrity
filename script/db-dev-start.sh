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
