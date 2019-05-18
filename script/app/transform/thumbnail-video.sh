#!/bin/bash

FRAME=$1
INPUT_PATH=$2
OUTPUT_PATH=$3
SUPPRESS_LOGS=$4

if [ -z ${FRAME} ]; then
  echo "INPUT_PATH is required as the second argument"
  exit 1
fi

if [ -z ${INPUT_PATH} ]; then
  echo "INPUT_PATH is required as the second argument"
  exit 1
fi

if [ -z ${OUTPUT_PATH} ]; then
  echo "OUTPUT_PATH is required as the third argument"
  exit 1
fi

if [ -z ${SUPPRESS_LOGS} ]; then
  echo "SUPPRESS_LOGS is required as the fourth argument"
  exit 1
fi

if [ ${SUPPRESS_LOGS} -eq 1 ]; then
  SUPPRESS_LOGS=" -nostats -loglevel 0"
else
  SUPPRESS_LOGS=""
fi

ffmpeg -ss $FRAME -i "${INPUT_PATH}" -vframes 1 -filter:v 'yadif,scale=100:100' "${OUTPUT_PATH}" -y ${SUPPRESS_LOGS}
