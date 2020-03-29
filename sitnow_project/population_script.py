import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'sitnow_project.settings')

import django
django.setup()

import requests

from django.contrib.auth.models import User
from sitnow.models import Comment, Place, UserProfile
from sitnow_project.config import keys
import time
from django.core.files.images import ImageFile
from sitnow_project.settings import BASE_DIR
from csv_2_json import *


GOOGLE_API_KEY = keys.GOOGLE_API_KEY
# Get google place id here: https://developers.google.com/places/place-id


def populate():
    # Create test dataset in a list
    users = [{
        'username': 'elliot.alderson', 'password': 'uB82uVhq423S0bw',
        'email': 'elliot.alderson@notrealemail.uk', 'preferred_name': 'Mr. Robot', 'img': 'sitnow_project/media/profile_images/profile_img_1.jpg'},
        {'username': 'gregory.house', 'password': 'cKXtpKNtxwRGMmoHL2kzCVWW9TBnoOdfnxNT',
         'email': 'gregory.house@notrealemail.uk', 'preferred_name': 'House M.D.', 'img': 'sitnow_project/media/profile_images/profile_img_2.jpg'},
        {'username': 'fiona.gallagher', 'password': 'R4RLB1Ry',
         'email': 'fiona.gallagher@notrealemail.uk', 'preferred_name': 'Gallagher', 'img': 'sitnow_project/media/profile_images/profile_img_3.jpg'}, ]

    PLACES_JSON_PATH = os.path.join(BASE_DIR, "sitnow_project", "places.json")
    places = read_json(PLACES_JSON_PATH)

    comments = [{'rate': 5, 'comment': 'Food is good for students with good price.'},
                {'rate': 1, 'comment': 'No food allergy warnings. Always crowded.'},
                {'rate': 3, 'comment': 'a cozy place WITHOUT eduroam wifi signal'},
                {'rate': 3, 'comment': 'Our democracy has been hacked.'},
                {'rate': 1, 'comment': 'Is the heater broken???'},
                {'rate': 2, 'comment': 'Please do not eat here guys!'}, ]

    user_objects, places_objects = [], []

    for user in users:
        user_objects.append(add_user(user))
    for place in places:
        places_objects.append(add_place(place))

    add_comment(user_objects[0], places_objects[0], comments[0])
    add_comment(user_objects[1], places_objects[0], comments[1])
    add_comment(user_objects[0], places_objects[5], comments[2])
    add_comment(user_objects[0], places_objects[6], comments[3])
    add_comment(user_objects[1], places_objects[6], comments[4])
    add_comment(user_objects[2], places_objects[6], comments[5])


def add_user(user):
    print('Populating user: ' + user['username'])
    u = User.objects.get_or_create(
        username=user['username'], email=user['email'])[0]
    u.set_password(user['password'])
    u_profile = UserProfile.objects.get_or_create(
        user=u, preferred_name=user['preferred_name'])[0]
    u_profile.picture = ImageFile(
        open(os.path.join(BASE_DIR, user['img']), "rb"))
    u.save()
    u_profile.save()
    return u


def add_comment(user, place, comment):
    print('Populating comment: ' + comment['comment'])
    c = Comment.objects.get_or_create(
        user=user, place=place, rate=comment['rate'], comment=comment['comment'])[0]
    c.save()
    return c


def add_place(place):
    print('Populating place: ' + place['name'] + ' @ ' + place['building'])
    p = Place.objects.get_or_create(name=place['name'],
                                    google_id=place['google_id'],
                                    building=place['building'])[0]
    # google_place_id = place['google_id']
    # result = get_info_by_place_id(google_place_id)
    # p.latitude = result['geometry']['location']['lat']
    # p.longitude = result['geometry']['location']['lng']
    # p.address = result['formatted_address']
    p.latitude = place['latitude']
    p.longitude = place['longitude']
    p.address = place['address']

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


def get_info_by_place_id(google_id):
    place_details_url = ' https://maps.googleapis.com/maps/api/place/details/json?place_id=' + \
        google_id + '&language=en&key=' + GOOGLE_API_KEY
    # print(place_details_url)
    res = requests.get(place_details_url).json()
    time.sleep(5)
    return res['result']


# Start execution here!
if __name__ == '__main__':
    print('Population script starts...')
    populate()
    print('Population script ends.')
