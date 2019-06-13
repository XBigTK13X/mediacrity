#! /bin/bash

YOUTUBEDL_DIR=$1
URL=$2

if [ -z ${YOUTUBEDL_DIR} ]; then
  echo "Youtube dl dir is required as the first argument"
  exit 1
fi

if [ -z ${URL} ]; then
  echo "URL is required as the second argument"
  exit 1
fi

./youtube-dl -f best -o "$YOUTUBEDL_DIR/%(title)s.%(ext)s" "$URL"
