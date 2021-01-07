#!/usr/bin/env bash

sh scripts/run_django_asgi.sh
sh scripts/run_django_wsgi.sh
docker exec -ti django-wsgi sh -c "gunicorn --bind 0.0.0.0:8000 GoldDigger.wsgi"