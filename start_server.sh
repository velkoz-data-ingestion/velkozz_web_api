#!/bin/bash

# Collecting static files:
echo "Performing Static File Collection"
python manage.py collectstatic --noinput

# Applying Database Migrations:
python manage.py makemigrations
python manage.py migrate 

# Starting Server:
python manage.py runserver 0.0.0.0:8000