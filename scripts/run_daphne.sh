#!/usr/bin/env bash
docker exec -ti gold-digger-web-8001 sh -c "python3 manage.py makemigrations"
docker exec -ti gold-digger-web-8001 sh -c "python3 manage.py migrate"
docker exec -ti gold-digger-web-8001 sh -c "daphne -b 0.0.0.0 -p 8001 GoldDigger.asgi:application"
