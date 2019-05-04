#! /bin/bash

source $MEDIACRITY_CONFIG

docker rm -f mediacrity-db

sudo rm -rf $MEDIACRITY_DB_DATA_DIR

if [ ! -z $1 ]; then
  script/db/dev-start.sh
  sleep 5s
  script/db/migrate.sh
  cd web
  python manage.py createsuperuser
  cd ..
fi
