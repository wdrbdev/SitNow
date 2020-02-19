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
# username: admin
# psw: m34TYfbprixwE4mijO4xMnz2FI9UnkB9

# Setup of PythonAnywhere NGINX webserver
# Set pythonanywhere virtualenv as /home/letsgo/.virtualenvs/letsgoenv
# Set pythonanywhere code source as /home/letsgo/Lets-Go/lets_go_project


