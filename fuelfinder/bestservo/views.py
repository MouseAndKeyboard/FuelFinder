from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib3
from math import radians, cos, sin, asin, sqrt
import xmltodict
import pandas as pd
import traceback
import json
from django.views.decorators.csrf import csrf_exempt


def distance(lat1, lat2, lon1, lon2):
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (abs(c * r))
    
def get_best_servo(path, stations, max_diversion, km_per_l, desired_tank, current_tank, rac, woolies):
    distances = []
    for i in range(len(path)-1):
        distance = bestStation(path[i], path[i+1], stations, max_diversion, km_per_l, desired_tank, current_tank)
        distances.append(distance)
    sorted(distances, key=lambda r: r[2])
    return distances[0]

def bestStation(startPos, endPos, stations, maxDiversion=5, km_per_l=16.5, desired_amt=50, currAmt = 1, hasRACDiscount=False, hasWoolieDiscount=False):
    distances = []
    RACStations = set(['Puma','Caltex','Better Choice'])
    WooliesStations = set(['Ampol','EG Ampol','Caltex','Caltex Woolworths'])
    for index, row in stations.iterrows():
        station = []
        station.append(row['address'])

        if hasRACDiscount and hasWoolieDiscount:
            if row['brand'] in RACStations.union(WooliesStations):
                row['price'] = str(float(row['price']) - 4)

        elif hasRACDiscount:
            if row['brand'] in RACStations:
                row['price'] = str(float(row['price']) - 4)

        elif hasWoolieDiscount:
            if row['brand'] in WooliesStations:
                row['price'] = str(float(row['price']) - 4)


        d1 = distance(startPos[0], row['latitude'], startPos[1], row['longitude'])
        d2 = distance(endPos[0], row['latitude'], endPos[1], row['longitude'])
        d3 = distance(startPos[0], endPos[0], startPos[1], endPos[1])
        diversion = d1+d2 - d3


        # Filter out locations we cant reach with our current fuel
        if(d1 > currAmt*km_per_l):
            continue

        # Filter out locations above our max diversion distance
        if(maxDiversion < diversion):
            continue

        tank_at_servo = currAmt - d1 * (1/km_per_l)
        spent_at_servo = (desired_amt - tank_at_servo) * float(row['price'])
        final_leg_price = float(row['price']) # assumption
        final_leg_cost  = d2 * (1/km_per_l) * final_leg_price

        total_cost = spent_at_servo + final_leg_cost

        station.append((row['latitude'], row['longitude']))

        station.append(diversion)

        station.append(total_cost)

        distances.append(station)

    sorted(distances, key=lambda r: r[2])
    return distances[0]


def getfuel_df():
    url = "https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?"
    http = urllib3.PoolManager()

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    response = http.request('GET', url, headers={'User-Agent':user_agent,})

    try:
        data = xmltodict.parse(response.data)
        return pd.DataFrame(data['rss']['channel']['item'])

    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())

    return None


@csrf_exempt
def index(request):
    print(request)
    STATIONS = getfuel_df()

    if request.method == 'POST':
        body = json.loads(request.body)
        path = body['path']
        max_diversion = 5.0 # default
        km_per_l = float(body['efficiency'])
        desired_tank = float(body['capacity'])
        current_tank = float(body['current_tank'])
        RAC_disc = bool(int(body['RAC']))
        Woolies_disc = bool(int(body['Woolies']))
        print(path, max_diversion, km_per_l, desired_tank, current_tank, RAC_disc, Woolies_disc)
        servo = get_best_servo(path, STATIONS, max_diversion, km_per_l, desired_tank, current_tank, RAC_disc, Woolies_disc)
        print(servo)
        return JsonResponse(servo, safe=False)

    return JsonResponse({})

# Create your views here.
