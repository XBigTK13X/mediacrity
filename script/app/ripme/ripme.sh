#! /bin/bash

RIPS_DIR=$1
URL=$2

if [ -z ${RIPS_DIR} ]; then
  echo "Rips dir is required as the first argument"
  exit 1
fi

if [ -z ${URL} ]; then
  echo "URL is required as the second argument"
  exit 1
fi

cp rip-base.properties rip.properties

java \
  -jar ./ripme-1.7.84.jar \
  -d \
  -l "${RIPS_DIR}" \
  -u "${URL}"

rm rip.properties
