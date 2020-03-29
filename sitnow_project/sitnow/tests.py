from django.test import TestCase
from sitnow.models import Comment, Place
from sitnow.utils import get_places
from population_script import add_place
from django.forms.models import model_to_dict


# Test for calculation of distance by Google Directions API
class test_google_distance(TestCase):
    def setUp(self):
        places = [
            {'name': 'Main Library',
             'building': 'Glasgow University Library',
             'google_id': 'ChIJ615vB81FiEgR8IC4Yq2kyY8',
             'latitude': 55.8733667,
             'longitude': -4.2889457},
            {'name': 'Adam Smith Business School Library',
             'building': 'Adam Smith Building',
             'google_id': 'ChIJ-eWF3c1FiEgRkezEd5t9xkc',
             'latitude': 55.8737664,
             'longitude': -4.2898664}, ]
        for place in places:
            p = Place.objects.create(name=place['name'], building=place['building'],
                                     google_id=place['google_id'],
                                     latitude=place['latitude'],
                                     longitude=place['longitude'])
            p.save()

    # At the back of the library, it's closer to library according to the euclidean distance but farther to library than the Adam Smith building according to actual walking time calculated google map.
    def test_distance(self):
        test_search = {'latitude': 55.873583,
                       'longitude': -4.289177,
                       }
        places = Place.objects.all().order_by('-id')
        places = get_places.get_k_nearest(test_search, places, 5)
        self.assertEqual(places[0].building, 'Glasgow University Library')

        places = get_places.get_google_k_nearest(test_search, places, 3)
        self.assertEqual(places[0].building, 'Adam Smith Building')


# Test for calculation of the Euclidean distance
class test_euclidean_distance(TestCase):
    def setUp(self):
        places1 = [{
            # Student Service @Fraser Building
            "name": "Place1.1",
            "building": "Building1",
            "google_id": "ChIJs2n0CtJFiEgRdLveBYNVzjk",
            "latitude": 55.873081,
            "longitude": -4.287935299999999,
        }, {
            # Food for thought & Food to go @Fraser Building
            "name": "Place1.2",
            "building": "Building1",
            "google_id": "ChIJs2n0CtJFiEgRdLveBYNVzjk",
            "latitude": 55.873183,
            "longitude": -4.288289,
        }]
        places2 = [
            {
                # Common Room @ Queen Margaret Union
                "name": "Place2.1",
                "building": "Building1",
                "google_id": "ChIJV03TEs5FiEgR8VtLsutgOa4",
                "latitude": 55.87370989999999,
                "longitude": -4.2917144,
            }, {
                # Study Space @Queen Margaret Union
                "name": "Building1",
                "building": "Building1",
                "google_id": "ChIJV03TEs5FiEgR8VtLsutgOa4",
                "latitude": 55.87386,
                "longitude": -4.291395,
            }
        ]
        places3 = [{
            # The Hunterian Collections Study Centre @Kelvin Hall
            "name": "Place3.1",
            "building": "",
            "google_id": "ChIJhRwc-tBFiEgRbLs3EJOuEig",
            "latitude": 55.869109,
            "longitude": -4.292811,
        }, {
            # Kelvin Hall Cafe @Kelvin Hall
            "name": "Place3.2",
            "building": "",
            "google_id": "ChIJhRwc-tBFiEgRbLs3EJOuEig",
            "latitude": 55.86900070000001,
            "longitude": -4.2932081,
        }, ]

        # Save places into DB
        all_places = [places1, places2, places3]
        for places in all_places:
            for place in places:
                p = Place.objects.create(name=place['name'], building=place['building'],
                                         google_id=place['google_id'],
                                         latitude=place['latitude'],
                                         longitude=place['longitude'])
                p.save()

    # Each place's nearest location would be other places in the same building
    def test_distance(self):
        PLACES = []
        for place in list(Place.objects.all()):
            PLACES.append(model_to_dict(place))

        for place in PLACES:
            nearest_places = get_places.get_k_nearest(
                place, list(Place.objects.all()), 2)
            for nearest_place in nearest_places:
                self.assertEqual(nearest_place.building, place['building'])


# Test whether the get_places.place_filter() works correctly
class test_filter(TestCase):
    def setUp(self):
        restaurants = [
            {
                # Beer Bar @Glasgow University Union
                "name": "Restaurant",
                "building": "Restaurant",
                "level": 1,
                "google_id": "ChIJ3SIsZltFiEgRVjcb8D94KPE",
                "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/fdkOkHqFfPjwoSptRglM9A/o.jpg",
                "permission": "None",
                "hasTable": True,
                "hasWifi": True,
                "capacity": 80,
                "hasMicrowave": False,
                "hasSocket": False,
                "hasFood": True,
                "noEating": False,
                "hasCoffee": True,
                "hasComputer": False,
                "latitude": 55.872402,
                "longitude": -4.285164,
                "address": "32 University Ave, Glasgow G12 8LX, UK"
            }, {
                # Food for thought & Food to go @Fraser Building
                "name": "Restaurant",
                "building": "Restaurant",
                "level": 3,
                "google_id": "ChIJs2n0CtJFiEgRdLveBYNVzjk",
                "image_url": "https://payload.cargocollective.com/1/6/208556/2971675/Glasgow-Fraser-Building-4.jpg",
                "permission": "None",
                "hasTable": True,
                "hasWifi": True,
                "capacity": 400,
                "hasMicrowave": True,
                "hasSocket": True,
                "hasFood": True,
                "noEating": False,
                "hasCoffee": True,
                "hasComputer": False,
                "latitude": 55.873183,
                "longitude": -4.288289,
                "address": "65 Hillhead St, Glasgow G12 8QF, UK"
            }
        ]

        studying_places = [{
            # Main Library @Glasgow University Library
            "name": "Studying Place",
            "building": "Studying Place",
            "google_id": "ChIJ615vB81FiEgR8IC4Yq2kyY8",
            "hasTable": True,
            "hasWifi": True,
            "capacity": 2322,
            "hasMicrowave": False,
            "hasSocket": True,
            "hasFood": False,
            "noEating": True,
            "hasCoffee": False,
            "hasComputer": True,
            "latitude": 55.8733426,
            "longitude": -4.289248,
            "address": "University Of Glasgow, Hillhead St, Glasgow G12 8QE, UK"
        }, {  # McMillan Round Reading Room
            "name": "Studying Place",
            "building": "Studying Place",
            "google_id": "ChIJVdE7ic1FiEgRf_rCeHQLg6U",
            "hasTable": True,
            "hasWifi": True,
            "capacity": 351,
            "hasMicrowave": False,
            "hasSocket": True,
            "hasFood": False,
            "noEating": True,
            "hasCoffee": False,
            "hasComputer": True,
            "latitude": 55.872741,
            "longitude": -4.287971,
            "address": "University Ave, Glasgow G12 8QF"
        }]
        all_places = [restaurants, studying_places]

        for places in all_places:
            for place in places:
                p = Place.objects.create(name=place['name'],
                                         building=place['building'],
                                         google_id=place['google_id'],
                                         latitude=place['latitude'],
                                         longitude=place['longitude'],
                                         hasTable=place['hasTable'],
                                         hasWifi=place['hasWifi'],
                                         capacity=place['capacity'],
                                         hasMicrowave=place['hasMicrowave'],
                                         hasSocket=place['hasSocket'],
                                         hasFood=place['hasFood'],
                                         noEating=place['noEating'],
                                         hasCoffee=place['hasCoffee'],
                                         hasComputer=place['hasComputer'])
                p.save()

    # To find a studying place with table, wifi and socket but not providing food. The result should be places in the studying_places list above
    def test_find_studying_places(self):
        search_studying_places = {
            'hasTable': True,
            'hasWifi': True,
            'capacity': 0,
            'hasMicrowave': None,
            'hasSocket': True,
            'hasFood': None,
            'hasCoffee': None,
            'noEating': True,
            'hasComputer': None
        }

        places = get_places.place_filter(search_studying_places)
        self.assertEqual(len(list(Place.objects.all())), 4)
        self.assertEqual(len(places), 2)
        for place in places:
            self.assertEqual(place.name, "Studying Place")

    # To find a place to eat, where provides food and coffee. The result should be places in the restaurants list above
    def test_find_restaurant(self):
        search_restaurants = {
            'hasTable': True,
            'hasWifi': None,
            'capacity': 0,
            'hasMicrowave': None,
            'hasSocket': None,
            'hasFood': True,
            'hasCoffee': True,
            'noEating': None,
            'hasComputer': None
        }

        places = get_places.place_filter(search_restaurants)
        self.assertEqual(len(list(Place.objects.all())), 4)
        self.assertEqual(len(places), 2)
        for place in places:
            self.assertEqual(place.name, "Restaurant")

    # Give a search criteria for no search result. For example, no place will provide food but don't allow eating inside in our dataset. The number of result would be 0 in this case.
    def test_find_non_exist_place(self):
        search_restaurants = {
            'hasTable': None,
            'hasWifi': None,
            'capacity': 0,
            'hasMicrowave': None,
            'hasSocket': None,
            'hasFood': True,
            'hasCoffee': True,
            'noEating': True,
            'hasComputer': None
        }

        places = get_places.place_filter(search_restaurants)
        self.assertEqual(len(list(Place.objects.all())), 4)
        self.assertEqual(len(places), 0)
