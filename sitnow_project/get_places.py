import sys
path = sys.path.append('../')
if path not in sys.path:
    sys.path.append(path)

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sitnow_project.settings')

import django
django.setup()

import requests
from django.contrib.auth.models import User
from sitnow.models import Comment, Place, UserProfile
from django.forms.models import model_to_dict
from sitnow_project.config import keys
import heapq
import time
from math import sqrt
from string import Template


def distance(current_location, destination_place):
    return sqrt((current_location['latitude'] - destination_place.latitude)**2 + (current_location['longitude'] - destination_place.longitude)**2)


def filter(current_location):
    filter = {}
    for key, value in current_location.items():
        if(key is '_state'):
            continue

        if(value == None):
            filter_list = [True, False]
        else:
            filter_list = [value]

        filter[key] = filter_list

    places = Place.objects.filter(hasTable__in=filter['hasTable'],
                                  hasWifi__in=filter['hasWifi'],
                                  capacity__range=(
                                      filter['capacity'][0], sys.maxsize),
                                  hasMicrowave__in=filter['hasMicrowave'],
                                  hasSocket__in=filter['hasSocket'],
                                  hasFood__in=filter['hasFood'],
                                  hasCoffee__in=filter['hasCoffee'],
                                  noEating__in=filter['noEating'],
                                  hasComputer__in=filter['hasComputer'])

    return list(places)


def get_k_nearest(current_location, places, k=5):
    n_places = len(places)
    if(n_places < k):
        k = n_places

    # k_nearest = heapq.nsmallest(
    #     k, places, key=lambda p: distance(current_location, p))
    d = {}
    for place in places:
        d[place] = distance(current_location, place)
    print(heapq.nsmallest(
        k, d.items(), key=lambda p: p[1]))
    return heapq.nsmallest(
        k, places, key=lambda p: distance(current_location, p))


def google_distance(current_location, destination_place):
    url_template = 'https://maps.googleapis.com/maps/api/directions/json?origin=${start_latitude},${start_longitude}&destination=${end_latitude},${end_longitude}&mode=walking&language=en&key=${GOOGLE_API_KEY}'
    d = {'start_latitude': current_location['latitude'], 'start_longitude': current_location['longitude'],
         'end_latitude': destination_place.latitude, 'end_longitude': destination_place.longitude, 'GOOGLE_API_KEY': keys.GOOGLE_API_KEY}
    url = Template(url_template).substitute(d)
    print(url)
    res = requests.get(url).json()
    time.sleep(1)
    return round(res['routes'][0]['legs'][0]['duration']['value'] / 60)


def get_google_k_nearest(current_location, places, k=3):
    n_places = len(places)
    if(n_places < k):
        k = n_places

    d = {}
    # for place in places:
    #     d[place] = google_distance(current_location, place)
    # print(heapq.nsmallest(
    #     k, d.items(), key=lambda p: p[1]))
    return heapq.nsmallest(
        k, places, key=lambda p: google_distance(current_location, p))


if __name__ == "__main__":
    current_location = {'latitude': 55.873583,
                        'longitude': -4.289177,
                        'hasTable': True,
                        'hasWifi': True,
                        'capacity': 21,
                        'hasMicrowave': None,
                        'hasSocket': None,
                        'hasFood': None,
                        'hasCoffee': None,
                        'noEating': None,
                        'hasComputer': None}

    filtered_places = filter(current_location)
    print(filtered_places)

    k_nearset = get_k_nearest(current_location, filtered_places, 5)
    print(k_nearset)

    k_google_nearset = get_google_k_nearest(
        current_location, k_nearset, 3)
    print(k_google_nearset)
