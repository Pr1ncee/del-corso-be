#!/bin/bash

echo "Applying migrations..."
python del_corso/manage.py migrate
echo "All migrations applied!"

echo "Creating admin user..."
python del_corso/manage.py initadmin
echo "The admin user has successfully created!"

echo "Pre-filling the database with necessary data..."
python del_corso/manage.py prefilldb
echo "All the data created successfully!"

echo "Starting the server..."
python del_corso/manage.py runserver 0.0.0.0:8000