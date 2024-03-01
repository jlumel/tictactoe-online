#!/usr/bin/env bash
# exit on error
set -o errexit
gunicorn -b 0.0.0.0:10000 final_project.wsgi:application &
daphne -b 0.0.0.0 -p 443 final_project.asgi:application