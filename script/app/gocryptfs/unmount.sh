#! /bin/bash

MOUNT_PATH=$1

if [ -z ${MOUNT_PATH} ]; then
  echo "Mount path required as the first argument"
  exit 1
fi

fusermount -u $MOUNT_PATH/dec
