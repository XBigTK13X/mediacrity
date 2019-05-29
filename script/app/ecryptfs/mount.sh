#! /bin/bash

MOUNT_PATH=$1
PASSWORD=$2

if [ -z ${MOUNT_PATH} ]; then
  echo "Mount path required as the first argument"
  exit 1
fi

if [ -z ${PASSWORD} ]; then
  echo "Password required as the second argument"
  exit 1
fi

TEMP_FILE="/tmp/ecryptfs.txt"

printf "%s" "${PASSWORD}" | ecryptfs-add-passphrase > $TEMP_FILE

SIGNATURE=`tail -1 ${TEMP_FILE} |  awk '{print $6}' | sed 's/\[//g' | sed 's/\]//g'`

rm -f ${TEMP_FILE}

yes '' | mount -t ecryptfs -o key=passphrase:passphrase_passwd=${PASSWORD},no_sig_cache=yes,verbose=no,ecryptfs_sig=${SIGNATURE},ecryptfs_cipher=aes,ecryptfs_key_bytes=16,ecryptfs_passthrough=no,ecryptfs_enable_filename_crypto=yes ${MOUNT_PATH} ${MOUNT_PATH} > /dev/null 2>&1
