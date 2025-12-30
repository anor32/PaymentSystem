#!/bin/bash
set -e

mkdir -p /code/staticfiles

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata payments.json users.json --ignore

python manage.py collectstatic --noinput

exec gunicorn your_project.wsgi:application --bind 0.0.0.0:10000
