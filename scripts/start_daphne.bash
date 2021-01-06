#!/bin/bash

NAME="GoldDigger"  # Name of the application
DJANGODIR=/usr/src/app  # Django project directory
# DJANGOENVDIR=/home/ubuntu/webapp/myprojectenv  # Django project env

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
# cd $DJANGODIR
# source /home/ubuntu/webapp/myprojectenv/bin/activate
# source /home/ubuntu/webapp/myproject/proj/.env
# export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start daphne
exec daphne -u /usr/src/app/run/daphne.sock --access-log - --proxy-headers GoldDigger.asgi:application