#!/bin/bash

echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations helloworld --noinput
python3.9 manage.py migrate helloworld --noinput

echo "Running Tests..."
python3.9 manage.py test

echo "Linting..."
ruff check .

echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear