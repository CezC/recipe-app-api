FROM python:3.9-alpine3.13
LABEL maintainer="CezC"

# recommended for using withy python
# dont buffer output, print it on console right away to don't have delays 
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# it will be overwritten in docker-compose file.
ARG DEV=false

#we use virtualenv because there can be conflicts with pyton from base image with our requirements
# we upgrade pip in our venw
# we install requirements
# delete tmp files to have lighter docker image without our requirements
# add new django user to run django as nonroot
RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  # install postgesql-client package in other our psycopg2 package to connect postgresql it will stay 
  apk add --update --no-cache postgresql-client && \
  # it groups packages in virutal deps we will then remove this group build-base, posggresql-dev and musl-dev
  # those are needed to install psycopg2, psycopg2 we will put in requirements.txt
  # then docker compose build to rebuild requirements.txt with psycop2 added
  apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
  fi && \
  rm -rf /tmp && \
  # we remove our grouped packages thats are deps for installing psycopg2
  apk del .tmp-build-deps && \
  adduser \
    --disabled-password \
    --no-create-home \
    django-user

# update environment PATH variable add /py/bin
ENV PATH="/py/bin:$PATH"

# we switch to django-user (should be last line of out Dockerfile)
USER django-user

# command to test build this image
# docker build .


# then docker compose build to rebuild requirements.txt with psycop2 added