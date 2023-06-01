from orm import Model, Database
from urllib.parse import urlencode
import requests


class home_page_route(Model):
    route_id = str
    routes = str

    def __init__(self, route_id: str, routes: str):
        self.route_id = route_id
        self.routes = routes

    def __Str__(self):
        return self.route_id + "<->" + self.routes


class home_page_stops(Model):
    stop_name = str
    stop_lat = float
    stop_lon = float

    def __init__(self, stop_name: str):
        self.stop_name = stop_name
        self.stop_lat, self.stop_lon = self.getLatLong()

    def getLatLong(self) -> tuple:
        stop_name_for_google = self.stop_name + ", Mysore" if "Mysore" not in self.stop_name else self.stop_name
        print(stop_name_for_google)
        endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": stop_name_for_google, 'region': '.in', "key": "AIzaSyCsbns--l53kPssGVEYcCzfsfU4m83kaB4", }
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        req = requests.get(url)
        lat = req.json()['results'][0]['geometry']['location']['lat']
        lng = req.json()['results'][0]['geometry']['location']['lng']
        return (lat, lng)


db = Database("../IRBTS/db.sqlite3")
home_page_route.db = db
home_page_stops.db = db

routes = []

with open("route_raw_data.txt", "r") as raw_data:
    file_data = raw_data.readlines()
    for i in file_data:
        col = i.split("-")
        if len(col) > 2:
            col = ["-".join([col[0], col[1]]), col[2]]
        clean = ",".join(list(map(lambda x: x.strip(), col[1].split(","))))
        route = home_page_route(col[0], clean)
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