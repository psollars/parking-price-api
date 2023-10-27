#!/bin/sh

if [! -d .venv/bin/activate ]; then
  pipenv shell
  pipenv install
fi

python manage.py test
