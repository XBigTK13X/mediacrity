#! /bin/bash

source $MEDIACRITY_CONFIG

pg_dumpall -U $MEDIACRITY_DB_USER -h $MEDIACRITY_DB_HOST > mediacrity.sql
