web: cd gamezone && python manage.py migrate && python manage.py seed_gamezone --if-empty && python manage.py collectstatic --noinput && gunicorn gamezone.wsgi --log-file -
