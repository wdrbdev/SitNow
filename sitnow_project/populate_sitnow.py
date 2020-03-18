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

    # places = [
    #     {'name': 'Food for thought & Food to go',
    #      'building': 'The Fraser Building',
    #      'level': 3,
    #      'google_id': 'ChIJs2n0CtJFiEgRdLveBYNVzjk',
    #      'image_url': 'https://payload.cargocollective.com/1/6/208556/2971675/Glasgow-Fraser-Building-4.jpg',
    #      'permission': None,
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 400,
    #      'hasMicrowave': True,
    #      'hasSocket': True,
    #      'hasFood': True,
    #      'noEating': False,
    #      'hasCoffee': True,
    #      'hasComputer': False},
    #     {'name': 'Food in focus',
    #      'building': 'Glasgow University Library',
    #      'level': 3,
    #      'google_id': 'ChIJ615vB81FiEgR8IC4Yq2kyY8',
    #      'image_url': 'https://media.thetab.com/blogs.dir/11/files/2017/03/20170322-120045-e1491236301851.jpg',
    #      'permission': 'For studnets and staffs of Glasgow University only, tap your university ID card to access.',
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 150,
    #      'hasMicrowave': True,
    #      'hasSocket': True,
    #      'hasFood': True,
    #      'noEating': False,
    #      'hasCoffee': True,
    #      'hasComputer': False},
    #     {'name': 'Main Library',
    #      'building': 'Glasgow University Library',
    #      'level': 2,
    #      'google_id': 'ChIJ615vB81FiEgR8IC4Yq2kyY8',
    #      'image_url': 'https://www.gla.ac.uk/media/Media_334613_smxx.jpg',
    #      'permission': 'For studnets and staffs of Glasgow University only, tap your university ID card to access.',
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 2322,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': False,
    #      'hasCoffee': False,
    #      'hasComputer': True},
    #     {'name': 'Reading Room',
    #      'building': 'Glasgow University Library',
    #      'level': 1,
    #      'google_id': 'ChIJ615vB81FiEgR8IC4Yq2kyY8',
    #      'image_url': 'https://taylorandfraser.com/wp-content/uploads/2018/04/3O7A0689-782x475.jpg',
    #      'permission': 'For studnets and staffs of Glasgow University only, tap your university ID card to access.',
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 80,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': True,
    #      'hasCoffee': False,
    #      'hasComputer': True},
    #     {'name': 'McMillan Round Reading Room',
    #      'building': 'McMillan Round Reading Room',
    #      'level': 2,
    #      'google_id': 'ChIJVdE7ic1FiEgRf_rCeHQLg6U',
    #      'image_url': 'https://manchesterhistory.net/architecture/1930/roundlibrary8.jpg',
    #      'permission': None,
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 351,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': True,
    #      'hasCoffee': False,
    #      'hasComputer': True},
    #     {'name': 'Adam Smith Business School Library',
    #      'building': 'Adam Smith Building',
    #      'level': 4,
    #      'google_id': 'ChIJ-eWF3c1FiEgRkezEd5t9xkc',
    #      'image_url': 'https://universityofglasgowlibrary.files.wordpress.com/2016/02/15-027-adam-smith-library-010.jpg?w=2000',
    #      'permission': 'For studnets and staffs of Glasgow University only, tap your university ID card to access.',
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 60,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': True,
    #      'hasCoffee': False,
    #      'hasComputer': True},
    #     {'name': 'Miller the Cat Student Common Room',
    #      'building': 'Adam Smith Building',
    #      'level': 2,
    #      'google_id': 'ChIJ-eWF3c1FiEgRkezEd5t9xkc',
    #      'image_url': 'https://www.gla.ac.uk/media/Media_616977_smxx.jpg',
    #      'permission': None,
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 20,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': False,
    #      'hasCoffee': False,
    #      'hasComputer': True},
    #     {'name': 'Social Sciences Postgraduate Study Space',
    #      'building': 'Adam Smith Building',
    #      'level': 2,
    #      'google_id': 'ChIJ-eWF3c1FiEgRkezEd5t9xkc',
    #      'image_url': 'https://disabledgoimageslive.blob.core.windows.net/venues/86cc0484-9f50-584a-912e-e802bae55439/253b93b8-4f3b-9a48-9a5b-0aff185a53e9.jpg',
    #      'permission': 'Open to Postgraduate Law, Education and SPS students.',
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 90,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': True,
    #      'hasCoffee': False,
    #      'hasComputer': False},
    #     {'name': 'Common Room',
    #      'building': 'Hetherington Building',
    #      'level': 2,
    #      'google_id': 'ChIJjVaouM1FiEgR_QmN8kKGNVI',
    #      'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/b8bd64f1-f610-af43-9b26-23c73c0715b5/5bc6119b-f02c-f84e-945f-646d953b62b9.jpg',
    #      'permission': None,
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 20,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': False,
    #      'hasCoffee': False,
    #      'hasComputer': False},
    #     {'name': 'Atrium Café',
    #      'building': 'Wolfson Medical School Building',
    #      'level': 2,
    #      'google_id': 'ChIJqRkzI85FiEgRE66dkk22miA',
    #      'image_url': 'https://www.gla.ac.uk/media/Media_461629_smxx-640x420.jpg',
    #      'permission': None,
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 80,
    #      'hasMicrowave': True,
    #      'hasSocket': False,
    #      'hasFood': True,
    #      'hasCoffee': True,
    #      'noEating': False,
    #      'hasComputer': False},
    #     {'name': 'Common Room of Sir Alexander Stone Building',
    #      'building': 'Sir Alexander Stone Building',
    #      'level': 2,
    #      'google_id': 'ChIJHS6QC85FiEgRg4kfcZYiD1g',
    #      'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/efd4ac76-b463-1440-b6c3-652d8983528b/058fcf9a-6e99-614f-9960-4ba699a41b96.jpg',
    #      'permission': None,
    #      'hasTable': True,
    #      'hasWifi': False,
    #      'capacity': 15,
    #      'hasMicrowave': True,
    #      'hasSocket': False,
    #      'hasFood': False,
    #      'noEating': False,
    #      'hasCoffee': False,
    #      'hasComputer': False},
    #     {'name': 'Sofa area of Graham Kerr Building',
    #      'building': 'Graham Kerr Building',
    #      'level': 3,
    #      'google_id': 'ChIJ9UILxdFFiEgRcczDSTMY9Lc',
    #      'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/bdc81d97-344b-d244-89b7-232c207176e7/dd0b8ff2-431d-af4b-8e71-5874d562c941.jpg',
    #      'permission': None,
    #      'hasTable': False,
    #      'hasWifi': True,
    #      'capacity': 8,
    #      'hasMicrowave': False,
    #      'hasSocket': False,
    #      'hasFood': False,
    #      'noEating': False,
    #      'hasCoffee': False,
    #      'hasComputer': False},
    #     {'name': 'Lab 1028',
    #      'building': 'Boyd Orr Building',
    #      'level': 10,
    #      'google_id': 'ChIJ84mnP85FiEgRggBlYJGkBVc',
    #      'image_url': 'https://disabledgoimageslive.blob.core.windows.net/access-guides/bdc81d97-344b-d244-89b7-232c207176e7/dd0b8ff2-431d-af4b-8e71-5874d562c941.jpg',
    #      'permission': 'For CS studnets only, tap your student ID card to access',
    #      'hasTable': True,
    #      'hasWifi': True,
    #      'capacity': 100,
    #      'hasMicrowave': False,
    #      'hasSocket': True,
    #      'hasFood': False,
    #      'noEating': True,
    #      'hasCoffee': False,
    #      'hasComputer': True}, ]
    PLACES_JSON_PATH = os.path.join(BASE_DIR, "sitnow_project", "places.json")
    places = read_json(PLACES_JSON_PATH)

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
