#! /bin/bash

if [ ! -z $MEDIACRITY_DEV_CONTAINER ]; then
  /usr/bin/supervisord -c /mediacrity/app/script/docker/supervisord-services.conf
else
  /usr/bin/supervisord -c /mediacrity/app/script/docker/supervisord-full.conf
fi
