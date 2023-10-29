#!/bin/zsh

if [ ! -d .venv ]; then
  echo "Starting venv..."
  pipenv shell
  echo "Installing packages..."
  pipenv install
fi

echo "Running migrations..."
pipenv run python manage.py migrate

echo "Loading rates fixtures..."
pipenv run python manage.py loaddata rates/fixtures/rates_fixture.json

pipenv run python manage.py runserver 5000
