# import sys
# path = sys.path.append('../')
# if path not in sys.path:
#     sys.path.append(path)

# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',
#                       'sitnow_project.settings')

# import django
# django.setup()

import requests
from django.contrib.auth.models import User
from sitnow.models import Comment, Place, UserProfile
from django.forms.models import model_to_dict
from sitnow_project.config import keys
import heapq
import time
from math import sqrt
from string import Template


def distance(place1, place2):
    return sqrt((place1.latitude - place2.latitude)**2 + (place1.longitude - place2.longitude)**2)


def filter(places):
    # TODO add place filter
    return


def get_k_nearest(current_location, k=5):
    places = Place.objects.all()
    # TODO add filter
    # places = filter(places)

    n_places = places.count()
    if(n_places < k):
        k = n_places

    k_nearest = heapq.nsmallest(
        k, places, key=lambda p: distance(p, current_location))
    return k_nearest


def google_distance(place1, place2):
    url_template = 'https://maps.googleapis.com/maps/api/directions/json?origin=${start_latitude},${start_longitude}&destination=${end_latitude},${end_longitude}&mode=walking&language=en&key=${GOOGLE_API_KEY}'
    d = {'start_latitude': place1.latitude, 'start_longitude': place1.longitude,
         'end_latitude': place2.latitude, 'end_longitude': place2.longitude, 'GOOGLE_API_KEY': keys.GOOGLE_API_KEY}
    url = Template(url_template).substitute(d)
    res = requests.get(url).json()
    time.sleep(0.3)
    return round(res['routes'][0]['legs'][0]['duration']['value'] / 60)


def get_google_k_nearest(current_location, k=3):
    top_5_places = get_k_nearest(current_location, 5)

    n_places = len(top_5_places)
    if(n_places < k):
        k = n_places

    d = {}
    for place in top_5_places:
        d[place] = google_distance(current_location, place)
    return heapq.nsmallest(
        k, d.items(), key=lambda p: p[1])


if __name__ == "__main__":
    current_location = Place.objects.last()
    print(current_location)
    k_nearset = get_k_nearest(current_location, 3)
    print(k_nearset)
    print(get_google_k_nearest(current_location, 3))
