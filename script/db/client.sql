#! /bin/bash

source $MEDIACRITY_CONFIG

docker exec -it mediacrity-dev psql -U $MEDIACRITY_DB_USER -d $MEDIACRITY_DB_NAME
