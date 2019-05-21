#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

python manage.py runserver $MEDIACRITY_WEB_HOST:$MEDIACRITY_WEB_PORT
