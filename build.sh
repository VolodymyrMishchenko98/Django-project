#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python cinemaarch/manage.py collectstatic --no-input
python cinemaarch/manage.py migrate
