#!/bin/bash

redis-server &

service nginx start

gunicorn -b 0.0.0.0:10000 final_project.wsgi:application &
daphne -b 0.0.0.0 -p 8000 final_project.asgi:application

exec "$@"