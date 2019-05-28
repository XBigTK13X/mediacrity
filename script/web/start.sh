#! /bin/bash

set -e

MIGRATE=$1

source $MEDIACRITY_CONFIG

mkdir -p $MEDIACRITY_TEMP_DIR

if [ ! -z $MIGRATE ]; then
  script/db/migrate.sh
fi

echo "Starting web server"

cd web

python3 manage.py runserver $MEDIACRITY_WEB_HOST:$MEDIACRITY_WEB_PORT
