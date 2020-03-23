# Convert the JSON from the POST request of SearchForm to the input of get_places.place_filter()
def validate_querydict(querydict):
    d = {}
    querydict = querydict.dict()
    fields = ['latitude', 'longitude',
              'permission',
              'hasTable',
              'hasWifi',
              'capacity',
              'hasMicrowave',
              'hasSocket',
              'hasFood',
              'noEating',
              'hasCoffee',
              'hasComputer']

    # For 0-4 persons: No capacity limit
    # For 4-8 persons: Places with capacity > 12
    # For above 8 persons: Places with capacity > 31
    int_switcher = {'1': 0, '2': 12, '3': 31}
    boolean_switcher = {'None': None, 'True': True}
    for key, value in querydict.items():
        if key in fields:
            if key == 'latitude' or key == 'longitude':
                d[key] = float(value)
            elif key == 'capacity':
                d[key] = int_switcher.get(value)
            else:
                d[key] = boolean_switcher.get(value)
    return d
