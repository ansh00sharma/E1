#!/bin/bash

pip install setuptools
pip install -r requirements.txt

python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

# python3.9 manage.py collectstatic --noinput

# mv static staticfiles_build

