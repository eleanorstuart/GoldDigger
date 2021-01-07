#!/usr/bin/env bash

docker stop django-wsgi
docker rm django-wsgi
docker run --gpus all -ti --name django-wsgi --network=gold-digger-web --link redis1:redis -v ${PWD}:/usr/src/app gold-digger/gold-digger-dev sh -c "celery -A GoldDigger  worker -l INFO"
# docker exec -ti django-wsgi sh -c "gunicorn --bind 0.0.0.0:8000 GoldDigger.wsgi"