#!/usr/bin/env bash
docker stop redis1
docker stop gold-digger-dev
docker rm redis1
docker rm gold-digger-dev

docker run -d --name redis1 redis

docker run  --gpus all \
            -d \
            --name gold-digger-dev \
            --link redis1:redis \
            -p 8000:8000 \
            -v ${PWD}:/usr/src/app \
            -v ~/Desktop/Drives/ds-prog/EM-DATA/gd-for-analysis:/usr/src/local-images \
            gold-digger/gold-digger-dev \
            sh -c "celery -A GoldDigger  worker -l INFO"

# docker run --gpus all -d --name gold-digger-dev --link redis1:redis -p 8000:8000 -v ${PWD}:/usr/src/app gold-digger/gold-digger-dev sh -c "celery -A GoldDigger  worker -l INFO"
docker exec -d gold-digger-dev sh -c "python3 manage.py makemigrations"
docker exec -d gold-digger-dev sh -c "python3 manage.py migrate"
docker exec -d gold-digger-dev sh -c "python3 manage.py runserver 0.0.0.0:8000"