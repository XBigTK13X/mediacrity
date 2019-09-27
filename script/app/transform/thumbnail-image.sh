#!/bin/bash

INPUT_PATH=$1
OUTPUT_PATH=$2

if [ -z "${INPUT_PATH}" ]; then
  echo "INPUT_PATH is required as the first argument"
  exit 1
fi

if [ -z "${OUTPUT_PATH}" ]; then
  echo "OUTPUT_PATH is required as the second argument"
  exit 1
fi

convert "${INPUT_PATH}" -resize '100x100!' "${OUTPUT_PATH}"
