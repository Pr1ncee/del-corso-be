#!/bin/bash

echo "Applying migrations..."
python del_corso/manage.py migrate

echo "Starting development server..."
python del_corso/manage.py runserver 0.0.0.0:8000