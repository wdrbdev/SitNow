from random import randint
from datetime import datetime
import pytz

import requests

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sitnow_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from sitnow.models import Comment, Place, SearchHistory, UserProfile
from sitnow_project.config import keys
import time

GOOGLE_API_KEY = keys.GOOGLE_API_KEY
# Get google place id here: https://developers.google.com/places/place-id


def populate():
    # Create test dataset in a list
    users = [{
        'username': 'elliot.alderson', 'password': 'uB82uVhq423S0bw',
        'email': 'elliot.alderson@notrealemail.uk', 'preferred_name': 'Mr. Robot'},
        {'username': 'gregory.house', 'password': 'cKXtpKNtxwRGMmoHL2kzCVWW9TBnoOdfnxNT',
         'email': 'gregory.house@notrealemail.uk', 'preferred_name': 'House M.D.'},
        {'username': 'fiona.gallagher', 'password': 'R4RLB1Ry',
         'email': 'fiona.gallagher@notrealemail.uk', 'preferred_name': 'Gallagher'}, ]

    places = [
        {'name': 'Food for thought',
         'building': 'The Fraser Building',
         'level': 3,
         'google_id': 'ChIJs2n0CtJFiEgRdLveBYNVzjk',
         'image_url': None,
         'permission': None,
         'hasTable': True,
         'hasWifi': True,
         'capacity': 400,
         'hasMicrowave': True,
         'hasSocket': True,
         'hasFood': True,
         'noEating': False,
         'hasCoffee': True,
         'hasComputer': False},
        {'name': 'Food to go',
         'building': 'The Fraser Building',
         'level': 3,
         'google_id': 'ChIJs2n0CtJFiEgRdLveBYNVzjk',
         'image_url': None,
         'permission': None,
         'hasTable': True,
         'hasWifi': True,
         'capacity': 400,
         'hasMicrowave': True,
         'hasSocket': True,
         'hasFood': True,
         'noEating': False,
         'hasCoffee': True,
         'hasComputer': False},
        {'name': 'Food in focus',
         'building': 'Glasgow University Library',
         'level': 3,
         'google_id': 'ChIJ615vB81FiEgR8IC4Yq2kyY8',
         'image_url': 'https://media.thetab.com/blogs.dir/11/files/2017/03/20170322-120045-e1491236301851.jpg',
         'permission': 'For studnets and staffs of Glasgow University  only, tap your university ID card to access',
         'hasTable': True,
         'hasWifi': True,
         'capacity': 150,
         'hasMicrowave': True,
         'hasSocket': True,
         'hasFood': True,
         'noEating': False,
         'hasCoffee': True,
         'hasComputer': False},
        {'name': 'Atrium Café',
         'building': 'Wolfson Medical School Building',
         'level': 0,
         'google_id': 'ChIJqRkzI85FiEgRE66dkk22miA',
         'image_url': None,
         'permission': None,
         'hasTable': True,
         'hasWifi': True,
         'capacity': 80,
         'hasMicrowave': True,
         'hasSocket': False,
         'hasFood': True,
         'hasCoffee': True,
         'noEating': False,
         'hasComputer': False},
        {'name': 'Common Room of Sir Alexander Stone Building',
         'building': 'Sir Alexander Stone Building',
         'level': 3,
         'google_id': 'ChIJHS6QC85FiEgRg4kfcZYiD1g',
         'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/efd4ac76-b463-1440-b6c3-652d8983528b/058fcf9a-6e99-614f-9960-4ba699a41b96.jpg',
         'permission': None,
         'hasTable': True,
         'hasWifi': False,
         'capacity': 15,
         'hasMicrowave': True,
         'hasSocket': False,
         'hasFood': False,
         'noEating': False,
         'hasCoffee': False,
         'hasComputer': False},
        {'name': 'Sofa area of Graham Kerr Building',
         'building': 'Graham Kerr Building',
         'level': 2,
         'google_id': 'ChIJ9UILxdFFiEgRcczDSTMY9Lc',
         'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/bdc81d97-344b-d244-89b7-232c207176e7/dd0b8ff2-431d-af4b-8e71-5874d562c941.jpg',
         'permission': None,
         'hasTable': False,
         'hasWifi': True,
         'capacity': 8,
         'hasMicrowave': False,
         'hasSocket': False,
         'hasFood': False,
         'noEating': False,
         'hasCoffee': False,
         'hasComputer': False},
        {'name': 'Lab 1028',
         'building': 'Boyd Orr Building',
         'level': 10,
         'google_id': 'ChIJ84mnP85FiEgRggBlYJGkBVc',
         'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/bdc81d97-344b-d244-89b7-232c207176e7/dd0b8ff2-431d-af4b-8e71-5874d562c941.jpg',
         'permission': 'For CS studnets only, tap your student ID card to access',
         'hasTable': True,
         'hasWifi': True,
         'capacity': 100,
         'hasMicrowave': False,
         'hasSocket': True,
         'hasFood': False,
         'noEating': True,
         'hasCoffee': False,
         'hasComputer': True}, ]

    search_hostories = [
        {'time_stamp': datetime(2019, 10, 2, 15, 3, 1, tzinfo=pytz.timezone('Europe/London')),
         'latitude': 55.873533,
         'longitude': -4.288123,
         'hasTable': True,
         'hasWifi': True,
         'nPeople': 1,
         'hasMicrowave': None,
         'hasSocket': None,
         'hasFood': True,
         'canEat': True,
         'hasCoffee': True,
         'hasComputer': None},
        {'time_stamp': datetime(2019, 12, 25, 11, 23, 55, tzinfo=pytz.timezone('Europe/London')),
         'latitude': 55.873318,
         'longitude': -4.287936,
         'hasTable': True,
         'hasWifi': True,
         'nPeople': 1,
         'hasMicrowave': None,
         'hasSocket': None,
         'hasFood': True,
         'canEat': True,
         'hasCoffee': True,
         'hasComputer': None}
    ]

    comments = [{'rate': 5, 'comment': 'Food is good for students with good price.'},
                {'rate': 0, 'comment': 'No food allergy warnings. Always crowded.'},
                {'rate': 3, 'comment': 'a cozy place WITHOUT eduroam wifi signal'},
                {'rate': 3, 'comment': 'Our democracy has been hacked.'},
                {'rate': 1, 'comment': 'Is the heater broken???'},
                {'rate': 2, 'comment': 'Please do not eat here guys!'}, ]

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    user_objects, places_objects = [], []

    for user in users:
        user_objects.append(add_user(user))
    for place in places:
        places_objects.append(add_place(place))
    for search_hostory in search_hostories:
        add_search_hostory(user_objects[0], places_objects, search_hostory)

    add_comment(user_objects[0], places_objects[0], comments[0])
    add_comment(user_objects[1], places_objects[0], comments[1])
    add_comment(user_objects[0], places_objects[5], comments[2])
    add_comment(user_objects[0], places_objects[6], comments[2])
    add_comment(user_objects[1], places_objects[6], comments[2])
    add_comment(user_objects[2], places_objects[6], comments[2])


def add_user(user):
    u = User.objects.get_or_create(
        username=user['username'], password=user['password'], email=user['email'])[0]
    u_profile = UserProfile.objects.get_or_create(
        user=u, preferred_name=user['preferred_name'])[0]
    u.save()
    u_profile.save()
    return u


def add_comment(user, place, comment):
    c = Comment.objects.get_or_create(
        user=user, place=place, rate=comment['rate'], comment=comment['comment'])[0]
    c.save()
    return c


def add_place(place):
    p = Place.objects.get_or_create(name=place['name'],
                                    google_id=place['google_id'],
                                    building=place['building'])[0]

    google_place_id = place['google_id']
    result = get_info_by_place_id(google_place_id)
    p.latitude = result['geometry']['location']['lat']
    p.longitude = result['geometry']['location']['lng']
    p.address = result['formatted_address']

    p.level = place['level']
    p.image_url = place['image_url']
    p.permission = place['permission']
    p.hasTable = place['hasTable']
    p.hasWifi = place['hasWifi']
    p.capacity = place['capacity']
    p.hasMicrowave = place['hasMicrowave']
    p.hasSocket = place['hasSocket']
    p.hasFood = place['hasFood']
    p.noEating = place['noEating']
    p.hasCoffee = place['hasCoffee']
    p.hasComputer = place['hasComputer']
    p.save()
    return p


def add_search_hostory(user, places, search_history):
    s = SearchHistory.objects.get_or_create(user=user, place1=places[0], place2=places[1], place3=places[2],
                                            time_stamp=search_history['time_stamp'],
                                            latitude=search_history['latitude'],
                                            longitude=search_history['longitude'])[0]
    s.hasTable = search_history['hasTable']
    s.hasWifi = search_history['hasWifi']
    s.nPeople = search_history['nPeople']
    s.hasMicrowave = search_history['hasMicrowave']
    s.hasSocket = search_history['hasSocket']
    s.hasFood = search_history['hasFood']
    s.hasCoffee = search_history['hasCoffee']
    s.hasComputer = search_history['hasComputer']
    s.canEat = search_history['canEat']
    s.save()
    return s


def get_info_by_place_id(googld_id):
    place_details_url = ' https://maps.googleapis.com/maps/api/place/details/json?place_id=' + \
        googld_id + '&language=en&key=' + GOOGLE_API_KEY
    # print(place_details_url)
    res = requests.get(place_details_url).json()
    time.sleep(2)
    # print(res['result'])
    return res['result']


# Start execution here!
if __name__ == '__main__':
    print('Population script starts...')
    populate()
    print('Population script ends')
