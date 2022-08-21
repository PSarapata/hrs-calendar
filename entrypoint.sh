#!/bin/sh

# entrypoint.sh

# Verify if the database is connected
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Delete all the tables
python manage.py flush --no-input
# Do a new migrate
python manage.py migrate

exec "$@"
