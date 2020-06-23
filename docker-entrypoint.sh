#!/bin/bash

echo "Run tests"
python ./manage.py test fin.tests.test_api

echo "Collect static files"
python ./manage.py collectstatic --noinput

echo "Apply database migrations"
python ./manage.py migrate

echo "Starting server"
python ./manage.py runserver 0.0.0.0:8000