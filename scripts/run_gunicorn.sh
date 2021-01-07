#!/usr/bin/env bash
docker exec -ti django-wsgi sh -c "gunicorn --bind 0.0.0.0:8000 GoldDigger.wsgi"