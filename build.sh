#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

rm -r trainer/migrations
python manage.py collectstatic --no-input
python manage.py makemigrations trainer
python manage.py migrate