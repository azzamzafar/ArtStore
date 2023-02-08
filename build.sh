#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
if [ "$CREATE_SUPERUSER}" == "TRUE" ];
then
  python3 manage.py createsuperuser --no-input
fi
python3 manage.py collectstatic --no-input
