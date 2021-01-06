#!/usr/bin/env bash

docker stop gold-digger-web-8001
docker rm gold-digger-web-8001
docker run --gpus all -ti --name gold-digger-web-8001 --link redis1:redis -p 8001:8001 -v ${PWD}:/usr/src/app gold-digger/gold-digger-dev
