#!/usr/bin/env bash
../manage.py collectstatic
uwsgi --ini uwsgi.ini
