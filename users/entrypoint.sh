#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python -m uvicorn users.asgi:application --host 0.0.0.0 --port 8000
