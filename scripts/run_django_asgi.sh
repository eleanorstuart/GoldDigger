#!/usr/bin/env bash

docker stop django-asgi
docker rm django-asgi
docker run --gpus all -ti --name django-asgi --network=gold-digger-web --link redis1:redis -p 8001:8001 -v ${PWD}:/usr/src/app gold-digger/gold-digger-dev sh -c "daphne -b 0.0.0.0 -p 8001 GoldDigger.wsgi:application"
