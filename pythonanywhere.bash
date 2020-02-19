#!/bin/bash
##################################################
# Commands for initialize app in pythonanywhere
##################################################

# Install virtual environment
mkvirtualenv -p python3.7 letsgoenv
workon letsgoenv
# /home/letsgo/.virtualenvs/rangoenv/bin/pip
# pip install -r requirements.txt
pip install django==2.1.5
# deactivate

# Clone from GitHub
git clone https://github.com/lightcoker/Lets-Go

# Create database
python manage.py makemigrations letsgo
python manage.py migrate
python populate_rango.py
python manage.py createsuperuser

# Setup of PythonAnywhere NGINX webserver
# Set pythonanywhere virtualenv as /home/letsgo/.virtualenvs/letsgoenv
# Set pythonanywhere code source as /home/letsgo/Lets-Go/lets_go_project

# Change wsgi.py on pythonanywhere (/var/www/letsgo_pythonanywhere_com_wsgi.py) as below
# # This file contains the WSGI configuration required to serve up your
# # web application at http://letsgo.pythonanywhere.com/
# # It works by setting the variable 'application' to a WSGI handler of some
# # description.
# #
# # The below has been auto-generated for your Django project

# import os
# import sys
# # Add your project's directory the PYTHONPATH
# path = '/home/letsgo/Lets-Go/lets_go_project/'
# if path not in sys.path:
#     sys.path.append(path)

# # Move to the project directory
# os.chdir(path)

# # Tell Django where the settings.py module is located
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'letsgo_project.settings')

# import django
# # Set up Django -- let it instantiate everything!
# django.setup()

# import django.core.handlers.wsgi
# # Import the Django WSGI to handle requests
# application = django.core.handlers.wsgi.WSGIHandler()

