#!/bin/zsh

if [ ! -d .venv ]; then
  echo "Starting venv..."
  pipenv shell
  echo "Installing packages..."
  pipenv install
fi

pipenv run python manage.py test
