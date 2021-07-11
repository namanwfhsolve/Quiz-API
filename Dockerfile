FROM python:3.7-slim

ENV MICRO_SERVICE=/home/app/microservice
ENV APP_USER=naman

# RUN echo Hello $APP_USER
# RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory


RUN mkdir -p $MICRO_SERVICE
# RUN mkdir -p $MICRO_SERVICE/server/static

# where the code lives
WORKDIR $MICRO_SERVICE

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry

# copy project
COPY poetry.lock pyproject.toml ${MICRO_SERVICE}/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . ${MICRO_SERVICE}

# COPY ./entrypoint.sh $MICRO_SERVICE

# CMD ["/bin/bash", "/home/app/microservice/entrypoint.sh"]