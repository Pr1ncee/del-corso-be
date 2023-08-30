#!/bin/bash

echo "Applying migrations..."
python del_corso/manage.py migrate
echo "All migrations applied!"

echo "Creating admin user..."
python del_corso/manage.py initadmin
echo "The admin user has successfully created!"

echo "Starting development server..."
python del_corso/manage.py runserver 0.0.0.0:8000