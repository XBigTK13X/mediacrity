#! /bin/bash

cd web

source $MEDIACRITY_CONFIG

mkdir -p $MEDIACRITY_TEMP_DIR

python3 worker.py
