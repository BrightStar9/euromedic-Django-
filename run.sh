#!/bin/sh

RETRIES=5

until psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES-=1)) remaining attempts..."
  sleep 3
done

python manage.py migrate
#python manage.py search_index --populate -f
python manage.py runserver 0.0.0.0:8000