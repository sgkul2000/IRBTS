import os

import requests
from urllib.parse import urlencode
import json
from decouple import config
from home_page.models import Stops
import math
# api_key = os.environ.get("API_KEY")  # Get API Key From Your Device "System Environment Variable"


api_key = config('KEY2')

def find_nearby_google(name):
    stop_name_for_google = name + ", Mysore" if "Mysore" not in name else name
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": stop_name_for_google, 'region': '.in', "key": api_key, }
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    req = requests.get(url)
    lat = req.json()['results'][0]['geometry']['location']['lat']
    lng = req.json()['results'][0]['geometry']['location']['lng']
    nearby = search_nearby_places(lat, lng)
    return nearby[0] if len(nearby) != 0 else name

def nearby_approximation(lat, long, angle):
    earth_radius = 6371000
    range = 500
    lat_a = math.radians(lat)
    long_a = math.radians(long)
    angular_distance = range / earth_radius
    true_course = math.radians(angle)

    lat = math.asin(
        math.sin(lat_a) * math.cos(angular_distance) + math.cos(lat_a) * math.sin(angular_distance)
                        * math.cos(true_course)
    )

    dlon = math.atan2(
        math.sin(true_course) * math.sin(angular_distance)
        * math.cos(lat_a),
        math.cos(angular_distance) - math.sin(lat_a) * math.sin(lat))

    long = ((long_a + dlon + math.pi) % (math.pi * 2)) - math.pi

    return math.degrees(lat), math.degrees(long)

def point_is_in_range(curr, center, range):
    R = 6371000
    dLat = math.radians(center[0] - curr[0])
    dLon = math.radians(center[1] - curr[1])
    lat1 = math.radians(curr[0])
    lat2 = math.radians(center[1])
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c

    return d < range

def search_nearby_places(lat, long):
    la1, lo1 = nearby_approximation(lat, long, 0)
    la2, lo2 = nearby_approximation(lat, long, 90)
    la3, lo3 = nearby_approximation(lat, long, 180)
    la4, lo4 = nearby_approximation(lat, long, 270)
    result = Stops.objects.raw(f'''
        SELECT * FROM home_page_stops WHERE
        + stop_lat + " > " + {la3} + " AND "
        + stop_lat + " < " + {la1} + " AND "
        + stop_lon + " < " + {lo2} + " AND "
        + stop_lon + " > " + {lo4}
    ''')
    result_list = []
    for stop in result:
        if point_is_in_range((stop.stop_lat, stop.stop_lon), (lat, long), 500):
            result_list.append(stop.stop_name)
    return result_list

print(search_nearby_places(12.3, 76.6))
