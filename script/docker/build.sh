#! /bin/bash

cp script/docker/Dockerfile.template ./Dockerfile

docker build --tag mediacrity/mediacrity:latest .

rm ./Dockerfile
