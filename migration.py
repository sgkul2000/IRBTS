from orm import Model, Database
from urllib.parse import urlencode
import requests
from decouple import config
from random import randint
from json import dumps

api_key = config('KEY2')


class home_page_route(Model):
    route_id = str
    routes = str

    def __init__(self, route_id: str, routes: str):
        self.route_id = route_id
        self.routes = routes

    def __str__(self):
        return self.route_id + "<->" + self.routes


class home_page_businformation(Model):
    bus_id = int
    bus_name = str
    bus_source = str
    bus_destination = str
    bus_viaroad = str
    bus_type = str
    route_id_id = str

    def __init__(self, bus_id: int, bus_name: str, bus_source: str, bus_destination: str, bus_via_road: str, bus_type: str, route_id: str):
        self.bus_id = bus_id
        self.bus_name = bus_name
        self.bus_source = bus_source
        self.bus_destination = bus_destination
        self.bus_viaroad = bus_via_road
        self.bus_type = bus_type
        self.route_id_id = route_id


class home_page_stops(Model):
    stop_name = str
    stop_lat = float
    stop_lon = float

    def __init__(self, stop_name: str):
        self.stop_name = stop_name
        self.stop_lat, self.stop_lon = self.getLatLong()

    def getLatLong(self) -> tuple:
        stop_name_for_google = self.stop_name + ", Mysore" if "Mysore" not in self.stop_name else self.stop_name
        endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": stop_name_for_google, 'region': '.in', "key": api_key, }
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        req = requests.get(url)
        lat = req.json()['results'][0]['geometry']['location']['lat']
        lng = req.json()['results'][0]['geometry']['location']['lng']

        try:
            places_endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "key": api_key,
                "location": f"{lat},{lng}",
                "radius": 500,
                "keyword": "Bus stop"
            }
            params_encoded = urlencode(params)
            places_url = f"{places_endpoint}?{params_encoded}"

            resp = requests.get(places_url)
            lat = resp.json()["results"][0]["geometry"]["location"]["lat"]
            lng = resp.json()["results"][0]["geometry"]["location"]["lng"]
        except Exception as e:
            print(stop_name_for_google)
        return (lat, lng)


db = Database("../IRBTS/db.sqlite3")
home_page_route.db = db
home_page_stops.db = db
home_page_businformation.db = db

routes = []

alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("route_raw_data.txt", "r") as raw_data:
    file_data = raw_data.readlines()
    for i in file_data:
        col = i.split("-")
        if len(col) > 2:
            col = ["-".join([col[0], col[1]]), col[2]]
        clean = ",".join(list(map(lambda x: x.strip(), col[1].split(","))))
        route = home_page_route(col[0], clean)
        start, dest = route.routes.split(',')[0], route.routes.split(',')[-1]
        bus = home_page_businformation(
            randint(1000, 10000),
            (alphas[randint(0, 25)] + str(randint(10, 150))),
            start,
            dest,
            'somewhere',
            'nan',
            route.route_id
        )
        bus.save()
        routes.append(route)
        route.save()
    db.commit()

calculated_stops = []

for route in routes:
    stops = route.routes.split(",")
    for stop_row in stops:
        if stop_row in calculated_stops:
            continue
        stop = home_page_stops(stop_row)
        stop.save()
        calculated_stops.append(stop_row)
    db.commit()