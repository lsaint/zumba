#!/usr/bin/env bash
../manage.py collectstatic
uwsgi --reload /tmp/zumba.pid
