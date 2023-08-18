#!/bin/sh

DB_HOST=localhost
DB_USER=euromedik
DB_NAME=euromedik
RETRIES=5

docker-compose up -d --build -f docker-compose-local.yml

until psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES-=1)) remaining attempts..."
  sleep 3
done

python manage.py migrate

python manage.py runserver 0.0.0.0:8000