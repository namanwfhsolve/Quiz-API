# !/bin/bash
cd server
echo "Hello Naman!"
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn server.wsgi:application --bind 0.0.0.0:8000
