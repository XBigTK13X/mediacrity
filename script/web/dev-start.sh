#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

mkdir $MEDIACRITY_TEMP_DIR

chmod -R 777 $MEDIACRITY_TEMP_DIR

python manage.py runserver
