cd server
echo "Hello Naman!"
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py collectstatic --no-input
poetry run gunicorn server.wsgi:application --bind 0.0.0.0:8000}
