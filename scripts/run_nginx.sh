#!/usr/bin/env bash
docker stop nginx
docker rm nginx
docker run -ti -p 80:80 --network=gold-digger-web -v ${PWD}/server-config/nginx:/etc/nginx/conf.d/ --name nginx nginx
