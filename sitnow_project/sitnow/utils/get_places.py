import requests
from django.contrib.auth.models import User
from sitnow.models import Comment, Place, UserProfile
from django.forms.models import model_to_dict
from sitnow_project.config import keys
import heapq
import time
from math import sqrt
from string import Template
import sys


# Filter places according to users' choices
def place_filter(current_location):
    places = Place.objects.all()
    for key, value in current_location.items():
        if(key is '_state'):
            continue

        if(key == 'hasTable' and value == True):
            places = places.filter(hasTable=value)
        if(key == 'hasWifi' and value == True):
            places = places.filter(hasWifi=value)
        if(key == 'capacity' and value == True):
            places = places.filter(capacity__range=(value, sys.maxsize))
        if(key == 'hasMicrowave' and value == True):
            places = places.filter(hasMicrowave=value)
        if(key == 'hasSocket' and value == True):
            places = places.filter(hasSocket=value)
        if(key == 'hasCoffee' and value == True):
            places = places.filter(hasCoffee=value)
        if(key == 'noEating' and value == True):
            places = places.filter(noEating=value)
        if(key == 'hasComputer' and value == True):
            places = places.filter(hasComputer=value)

    return list(places)


# Calculate distance of each place according to the Euclidean distance from latitude and longitude
def distance(current_location, destination_place):
    return sqrt((current_location['latitude'] - destination_place.latitude)**2 + (current_location['longitude'] - destination_place.longitude)**2)


# Get the top k nearest places according to result of distance()
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


# Calculate distance of each place according to Google Directions API
def google_distance(current_location, destination_place):
    url_template = 'https://maps.googleapis.com/maps/api/directions/json?origin=${start_latitude},${start_longitude}&destination=${end_latitude},${end_longitude}&mode=walking&language=en&key=${GOOGLE_API_KEY}'
    d = {'start_latitude': current_location['latitude'], 'start_longitude': current_location['longitude'],
         'end_latitude': destination_place.latitude, 'end_longitude': destination_place.longitude, 'GOOGLE_API_KEY': keys.GOOGLE_API_KEY}
    url = Template(url_template).substitute(d)
    print(url)
    res = requests.get(url).json()
    time.sleep(0.2)
    return round(res['routes'][0]['legs'][0]['duration']['value'] / 60)


# Get the top k nearest places according to result of google_distance()
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
