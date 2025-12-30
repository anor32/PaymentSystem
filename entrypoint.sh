#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/payments.json
python manage.py loaddata fixtures/users.json
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000
