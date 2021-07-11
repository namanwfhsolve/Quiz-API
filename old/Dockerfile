FROM python:3.7-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# System deps:
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/


# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code/

EXPOSE 8000

# CMD [ "sh", "run.sh" ]
# CMD [ "poetry", "run", "python", "manage.py", "runserver" ,"0.0.0.0:8000" ]
