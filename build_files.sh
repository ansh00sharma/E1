pip install -r requirements.txt

python3 manage.py collectstatic --noinput

mv static staticfiles_build