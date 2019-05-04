#! /bin/bash

source $MEDIACRITY_CONFIG

docker exec -it mediacrity-db psql -U $MEDIACRITY_DB_USER -d $MEDIACRITY_DB_NAME
