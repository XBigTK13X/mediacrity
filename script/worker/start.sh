#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

mkdir -p $MEDIACRITY_TEMP_DIR

echo "Starting mediacrity worker"

python3 worker.py
