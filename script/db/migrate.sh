#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

python manage.py makemigrations media

python manage.py migrate
