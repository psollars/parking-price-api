#!/bin/sh

if [! -d .venv/bin/activate ]; then
  pipenv shell
  pipenv install
fi

echo "Loading rates fixtures..."
python manage.py loaddata rates/fixtures/rates_fixture.json

python manage.py runserver 5000
