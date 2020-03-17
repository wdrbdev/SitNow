from django.test import TestCase
# Create your tests here.
from sitnow.models import Comment, Place
import get_places
from populate_sitnow import add_place


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
            print(place['name'])
            p = Place.objects.create(name=place['name'], building=place['building'],
                                     google_id=place['google_id'],
                                     latitude=place['latitude'],
                                     longitude=place['longitude'])
            p.save()

    def test_distance(self):
        # At the back of the library, it's closer to library according to the euclidean distance but farther to library than the Adam Smith building according to actual walking time calculated google map.
        test_search = {'latitude': 55.873583,
                       'longitude': -4.289177,
                       }
        places = Place.objects.all().order_by('-id')
        places = get_places.get_k_nearest(test_search, places, 5)
        self.assertEqual(places[0].building, 'Glasgow University Library')
        places = get_places.get_google_k_nearest(test_search, places, 3)
        self.assertEqual(places[0].building, 'Adam Smith Building')

# TODO test pupolating script will get latitude, longitude, and address
# TODO test single filter
# TODO test multiple filter
# TODO test normal case of get distnance (in library, get library & in adam smith get adam smith )


class test_distance(TestCase):
    # def test_canEat_filter(self):
    def setUp(self):
        Place.objects.create(name="Random Library location 1", google_id="ChIJ615vB81FiEgR8IC4Yq2kyY8",
                             building="Glasgow University Library", latitude=55.873305, longitude=-4.288483)
        Place.objects.create(name="Random Library location 2", google_id="ChIJ615vB81FiEgR8IC4Yq2kyY8",
                             building="Glasgow University Library", latitude=55.873419, longitude=-4.289360)
        Place.objects.create(name="Random Library location 3", google_id="ChIJ615vB81FiEgR8IC4Yq2kyY8",
                             building="Glasgow University Library", latitude=55.873229, longitude=-4.289117)
        Place.objects.create(name="Random Adam Smith Building location 1", google_id="ChIJ-eWF3c1FiEgRkezEd5t9xkc",
                             building="Adam Smith Building", latitude=55.873611, longitude=-4.289927)
        Place.objects.create(name="Random Adam Smith Building location 2", google_id="ChIJ-eWF3c1FiEgRkezEd5t9xkc",
                             building="Adam Smith Building", latitude=55.873829, longitude=-4.289847)
        Place.objects.create(name="Random Adam Smith Building location 3", google_id="ChIJ-eWF3c1FiEgRkezEd5t9xkc",
                             building="Adam Smith Building", latitude=55.874106, longitude=-4.289724)

    def test_find_place_library(self):
        test_search = {'latitude': 55.873601,
                       'longitude': -4.288830, }
        places = Place.objects.all().order_by('-id')
        places = get_places.get_k_nearest(test_search, places, 5)
        places = get_places.get_google_k_nearest(test_search, places, 3)
        for place in places:
            self.assertEqual(place.building, "Glasgow University Library")

    def test_find_place_adam_smith_building(self):
        test_search = {'latitude': 55.873935,
                       'longitude': -4.290140, }
        places = Place.objects.all().order_by('-id')
        places = get_places.get_k_nearest(test_search, places, 5)
        places = get_places.get_google_k_nearest(test_search, places, 3)
        for place in places:
            self.assertEqual(place.building, "Adam Smith Building")
            # Place.objects.create(name=,google_id=,building=,latitude=,
            #                                longitude=,
            #                                 hasTable=,
            #    hasWifi=,
            #    capacity=,
            #    hasMicrowave=,
            #    hasSocket=,
            #    hasFood=,
            #    noEating=,
            #    hasCoffee=,
            #    hasComputer=)

# class (TestCase):
#     def set_up(self):
#         return Place.objects.create(name='The back of glasgow university library', latitude=55.873520,
#                                     longitude=-4.289588)


# class test_google_distance(TestCase):
#     def set_up(self):
#         return Place.objects.create(name='The back of glasgow university library', latitude=55.873520,
#                                     longitude=-4.289588)
