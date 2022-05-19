#!/bin/sh

set -e
set -x

if [ "$DEBUG" == "1" ]
  then
    if [ "$DJANGO_DB_ENGINE" = "django.db.backends.postgresql" ]
      then
          echo "Waiting for postgres..."

          while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
            sleep 0.1
          done

          echo "PostgreSQL started"
      fi
  else
    ./.venv/bin/python3 bookshelf/manage.py collectstatic --noinput
fi

./.venv/bin/python3 bookshelf/manage.py makemigrations --noinput
./.venv/bin/python3 bookshelf/manage.py migrate --noinput
./.venv/bin/python3 bookshelf/manage.py initadmin
./.venv/bin/python3 bookshelf/manage.py runserver 0.0.0.0:$PORT