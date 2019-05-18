#!/bin/bash

INPUT_PATH=$1
OUTPUT_PATH=$2
SUPPRESS_LOGS=$3
FALLBACK_MODE=$4

if [ -z ${INPUT_PATH} ]; then
  echo "INPUT_PATH is required as the first argument"
  exit 1
fi

if [ -z ${OUTPUT_PATH} ]; then
  echo "OUTPUT_PATH is required as the second argument"
  exit 1
fi

if [ -z ${SUPPRESS_LOGS} ]; then
  echo "SUPPRESS_LOGS is required as the third argument"
  exit 1
fi

if [ -z ${FALLBACK_MODE} ]; then
  echo "FALLBACK_MODE is required as the fourth argument"
  exit 1
fi

if [ ${SUPPRESS_LOGS} -eq 1 ]; then
  SUPPRESS_LOGS=" -nostats -loglevel 0"
else
  SUPPRESS_LOGS=""
fi

if [ ${FALLBACK_MODE} -eq 0 ]; then
  ffmpeg -i "${INPUT_PATH}" -movflags faststart -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -acodec copy "${OUTPUT_PATH}" -y "${SUPPRESS_LOGS}"
else
  ffmpeg -i "${INPUT_PATH}" -movflags faststart -strict -2 "${OUTPUT_PATH}" -y ${SUPPRESS_LOGS}
fi
