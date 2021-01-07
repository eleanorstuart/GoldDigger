#!/usr/bin/env bash
docker stop redis1
docker rm redis1
docker run -d --network=gold-digger-web --name redis1 redis
