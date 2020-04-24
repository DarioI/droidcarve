#!/bin/bash
export PYTHONUNBUFFERED=TRUE
source server/venv/bin/activate && cd server/ && gunicorn -b 0.0.0.0:1337 --log-level=info wsgi:app --workers=1 --threads=10 --timeout=1800
