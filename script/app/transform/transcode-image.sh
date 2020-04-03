#!/bin/bash

INPUT_PATH=$1
OUTPUT_PATH=$2
SUPPRESS_LOGS=$3

if [ -z "${INPUT_PATH}" ]; then
  echo "INPUT_PATH is required as the first argument"
  exit 1
fi

if [ -z "${OUTPUT_PATH}" ]; then
  echo "OUTPUT_PATH is required as the second argument"
  exit 1
fi

if [ -z ${SUPPRESS_LOGS} ]; then
  echo "SUPPRESS_LOGS is required as the third argument"
  exit 1
fi

if [ ${SUPPRESS_LOGS} -eq 1 ]; then
  SUPPRESS_LOGS=" -nostats -loglevel 0"
else
  SUPPRESS_LOGS=""
  set -x
fi

convert -auto-orient "${INPUT_PATH}" "${OUTPUT_PATH}"
