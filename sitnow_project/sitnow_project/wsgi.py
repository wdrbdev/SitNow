"""
WSGI config for sitnow_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import django.core.handlers.wsgi
import django
import os
import sys

# Add your project's directory the PYTHONPATH
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path = '/home/sitnow/tango_with_django_project/'
if path not in sys.path:
    sys.path.append(path)

# Move to the project directory
os.chdir(path)

# Tell Django where the settings.py module is located
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sitnow_project.settings")

# Set up Django -- let it instantiate everything!
django.setup()

# Import the Django WSGI to handle requests
application = django.core.handlers.wsgi.WSGIHandler()
