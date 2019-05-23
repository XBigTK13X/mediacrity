#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

mkdir -p $MEDIACRITY_TEMP_DIR

python3 manage.py runserver $MEDIACRITY_WEB_HOST:$MEDIACRITY_WEB_PORT
