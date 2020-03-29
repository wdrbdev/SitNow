import numpy as np
from pandas import read_csv
import os
from numpy import genfromtxt
from population_script import *
import json

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILDINGS_CSV_PATH = os.path.join(BASE_DIR, "sitnow_project", "buildings.csv")
BUILDINGS_JSON_PATH = os.path.join(
    BASE_DIR, "sitnow_project", "buildings.json")
PLACES_CSV_PATH = os.path.join(BASE_DIR, "sitnow_project", "places.csv")
PLACES_JSON_PATH = os.path.join(BASE_DIR, "sitnow_project", "places.json")


# Convert building information from csv to json
def buildings_csv_to_json():
    a = np.array(genfromtxt(BUILDINGS_CSV_PATH, delimiter=',',
                            encoding="UTF-8", names=True, dtype=None))
    building_id_dict = {}
    for row in a:
        building_id_dict[row[1]] = row[0]

    return building_id_dict


# Convert place information from csv to json
def places_csv_to_json():
    a = np.array(genfromtxt(PLACES_CSV_PATH, delimiter=',',
                            encoding="UTF-8", names=True, dtype=None))
    places = []
    for row in a:
        d = {}
        d['name'] = row[1]
        d['building'] = row[2]
        d['level'] = int(row[3])
        d['google_id'] = row[4]
        d['image_url'] = row[5]
        d['permission'] = row[6]
        d['hasTable'] = bool(row[7])
        d['hasWifi'] = bool(row[8])
        d['capacity'] = int(row[9])
        d['hasMicrowave'] = bool(row[10])
        d['hasSocket'] = bool(row[11])
        d['hasFood'] = bool(row[12])
        d['noEating'] = bool(row[13])
        d['hasCoffee'] = bool(row[14])
        d['hasComputer'] = bool(row[15])
        places.append(d)
    return places


# Call Google Place API to get latitude and longitude
def get_location_lat_lng(building_id_dict):
    places = []
    for key, value in building_id_dict.items():
        d = {}
        result = get_info_by_place_id(key)
        d['building'] = value
        d['latitude'] = result['geometry']['location']['lat']
        d['longitude'] = result['geometry']['location']['lng']
        places.append(d)
    return places


# Call Google Place API to get latitude, longitude and address
def get_place_lat_lng(places):
    for place in places:
        google_id = place['google_id']
        result = get_info_by_place_id(google_id)
        place['latitude'] = result['geometry']['location']['lat']
        place['longitude'] = result['geometry']['location']['lng']
        place['address'] = result['formatted_address']
    return places


# Write array of dict into json file
def write_json(json_array, json_path):
    with open(json_path, 'w', encoding='UTF-8') as f:
        json.dump(json_array, f, ensure_ascii=False, indent=4)


# Read json file
def read_json(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
        return data


if __name__ == "__main__":
    # Convert csv of buildings locations to json and get latitude and longitude from google map api
    # locations = get_location(buildings_csv_to_json())
    # write_json(locations,BUILDINGS_JSON_PATH)
    print(read_json(PLACES_JSON_PATH))

    # Convert csv of places information to json and get latitude and longitude from google map api
    # places = places_csv_to_json()
    # places = get_place_lat_lng(places)
    # write_json(places, PLACES_JSON_PATH)
    print(read_json(PLACES_JSON_PATH))
