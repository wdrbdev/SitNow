def validate_querydict(querydict):
    d = {}
    querydict = querydict.dict()
    print(querydict)
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

    int_switcher = {'1': 0, '2': 0, '3': 31}
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
