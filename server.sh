# cd server/
# poetry run python manage.py migrate
# gunicorn server.wsgi -b 0.0.0.0:8000

cd server
export APP_PORT=8000
echo "Hello Naman!"
echo "running on ${APP_PORT}"
poetry run python manage.py makemigrations
poetry run python manage.py migrate
# poetry run python manage.py initiate_admin &&
poetry run python manage.py collectstatic --no-input
poetry run gunicorn server.wsgi:application --bind 0.0.0.0:${APP_PORT}
