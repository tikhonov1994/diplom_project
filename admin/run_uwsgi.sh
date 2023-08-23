#!/usr/bin/env bash

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --no-input || true
python manage.py compilemessages -l en -l ru

set -e

chown www-data:www-data /var/log

uwsgi --strict --ini uwsgi.ini