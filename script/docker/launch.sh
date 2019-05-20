#! /bin/bash

if [ ! -f /mediacrity/config/mediacrity-settings.sh ]; then
    echo "/mediacrity/config is required as as mount. It must contain mediacrity-settings.sh with environment variable exports."
    exit -1
fi

source /mediacrity/config/mediacrity-settings.sh

PATH="$PATH:/usr/bin"

mkdir -p /mediacrity/log

cd /mediacrity

echo "Starting worker"
script/worker/dev-start.sh

echo "Starting web app"
script/web/dev-start.sh
