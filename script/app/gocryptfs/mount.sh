ount#! /bin/bash

MOUNT_PATH=$1
PASSWORD=$2

gocryptfs -allow_other -extpass "echo '$PASSWORD'" $MOUNT_PATH/enc $MOUNT_PATH/dec
