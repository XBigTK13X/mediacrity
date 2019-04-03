#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

python manage.py runserver
