from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from backendCode.geocoding import reverse_geocoding, geocoding_from_address
from backendCode.nearbyplaces import search_nearby_places, find_nearby_google
from home_page.models import BusInformation, Stops, Route
from backendCode.findBusByDirection import find_distance
from decouple import config
from json import loads, dumps
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.


def searchnearby_address(request):
    location = request.POST['userlocationaddress']
    text = config('KEY2')
    url = f"https://maps.googleapis.com/maps/api/js?key={text}&callback=initMap&libraries=&v=weekly"
    data = geocoding_from_address(location)
    nearby_list = search_nearby_places(data['lat'], data['lng'])
    print("nearby list: ", nearby_list)
    data.update({'nearlist': nearby_list})
    data.update({'text': url})
    return render(request, 'smartTracking/searchnearby.html', data)


def searchnearby_latlng(request):
    location = str(request.POST['userLocation'])
    lat, lng = location.split(sep=',', maxsplit=1)
    formatted_address = reverse_geocoding(location)
    nearby_list = search_nearby_places(float(lat), float(lng))
    text = config('KEY2')
    url = f"https://maps.googleapis.com/maps/api/js?key={text}&callback=initMap&libraries=&v=weekly"
    data = {
        'formatted_address': formatted_address,
        'nearlist': nearby_list,
        'text': url

    }
    # print(location)
    return render(request, 'smartTracking/searchnearby.html', data)


def finddirection(request):
    bus_list = []
    start = str(request.POST['from'])
    end = str(request.POST['to'])
    start = find_nearby_google(start)
    end = find_nearby_google(end)
    try:
        routes = Route.objects.all()
        route_containing_stops = []
        for route in routes:
            route_stops = route.routes.split(sep=',')
            if start in route_stops and end in route_stops:
                route_containing_stops.append(route)
        bus_list = []
        for route in route_containing_stops:
            bus = BusInformation.objects.get(route_id_id=route.route_id)
            bus_raw_route = route.routes.split(sep=',')
            for i in range(0, len(bus_raw_route)):
                if start.lower() == bus_raw_route[i].lower():
                    start_index = i
                if end.lower() == bus_raw_route[i].lower():
                    end_index = i
            # print('Start_index' + str(start_index))
            # print('End_index' + str(end_index))
            bus_route = []
            if start_index < end_index:
                for i in range(start_index, end_index+1):
                    bus_route.append(bus_raw_route[i])
            elif start_index > end_index:
                for i in range(end_index, start_index+1):
                    bus_route.append(bus_raw_route[i])
            else:
                bus_route.append(bus_raw_route[start_index])
            distance = find_distance(bus_route)
            # print(bus_route)
            list_route = []
            for i in range(0, len(bus_route), 2):
                if i + 1 == len(bus_route):
                    temp = (bus_route[i], None)
                else:
                    temp = (bus_route[i], bus_route[i + 1])
                list_route.append(temp)
            data = {
                'bus_id': bus.bus_id,
                'bus_name': bus.bus_name,
                'bus_route': list_route,
                'distance': distance
            }
            bus_list.append(data)
            length = len(bus_list)
        contex = {
            'From': start,
            'To': end,
            'Number_of_bus': length,
            'bus_list': bus_list,
        }
        return render(request, 'smartTracking/finddirection.html', contex)
    except:
        contex = {
            'check': 1,
            'From': start,
            'To': end,
            'Number_of_bus': 0
        }
        return render(request, 'smartTracking/finddirection.html', contex)


def findspecificbus(request):
    bus_name_from_user = str(request.POST['bus_name'])
    try:
        buses = BusInformation.objects.filter(bus_name__iexact=bus_name_from_user)
        bus = buses[0]
        start, end = bus.bus_source, bus.bus_destination
        routes = bus.route_id.routes
        routes = routes.split(sep=',')
        list_route = []
        for i in range(0, len(routes), 2):
            if i + 1 == len(routes):
                temp = (routes[i], None)
            else:
                temp = (routes[i], routes[i + 1])
            list_route.append(temp)

        text = config('KEY2')
        mapURL = f"https://maps.googleapis.com/maps/api/js?key={text}&callback=initMap&libraries=&v=weekly"
        data = {
            'check': 0,
            'bus_id': bus.bus_id,
            'bus_name': bus.bus_name,
            'start': start,
            'end': end,
            'routes': list_route,
            'mapURL': mapURL
        }
        return render(request, 'smartTracking/findspecificbus.html', data)

    except:
        data = {
            'check': 1,
            "error": bus_name_from_user
        }
        return render(request, 'smartTracking/findspecificbus.html', data)


def allbuses(request):
    buses = BusInformation.objects.all()
    buses_list = []
    for bus in buses:
        start, end = str(bus.bus_source), str(bus.bus_destination)
        routes = bus.route_id.routes
        routes = routes.split(sep=',')
        design = str(routes[0])
        for r in range(1, len(routes) - 1):
            design = design + '<->' + str(routes[r])
        data = {
            'bus_id': bus.bus_id,
            'bus_name': bus.bus_name,
            'start': start,
            'end': end,
            'routes': design
        }
        buses_list.append(data)
    contex = {
        'contex': buses_list
    }
    # print(routes)
    return render(request, 'smartTracking/allbuses.html', contex)

def driverPortal(request):
    return render(request, 'smartTracking/driverPortal.html', {})

@csrf_exempt
def getStops(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    bus_from_user = str(body.get('bus_name'))
    buses = BusInformation.objects.filter(bus_name__iexact=bus_from_user)
    print(body)
    bus = buses[0]
    routes = bus.route_id.routes
    routes = routes.split(sep=',')
    stops = []
    for route in routes:
        stop = Stops.objects.filter(stop_name=route.strip())[0]
        stops.append({
            "stop_name": stop.stop_name,
            "lat": stop.stop_lat,
            "long": stop.stop_lon
        })
    print(stops)
    return JsonResponse(stops, safe=False)

@csrf_exempt
def getEta(request):
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    etaTo = body.get('stop')
    curLocation = body.get('cur_location')
    print(body)
    endpoint = f"https://routes.googleapis.com/directions/v2:computeRoutes"
    url = f"{endpoint}"
    req = requests.post(url, json={
        "origin":{
            "location":{
                "latLng":{
                    "latitude": curLocation['lat'],
                    "longitude": curLocation['lng']
                }
            }
        },
        "destination":{
            "location":{
            "latLng":{
                "latitude": etaTo['lat'],
                "longitude": etaTo['long']
            }
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "departureTime": "2023-10-15T15:01:23.045123456Z",
        "computeAlternativeRoutes": False,
        }, headers={
            "X-Goog-Api-Key": config('KEY2'),
            "Content-Type": "application/json",
            "X-Goog-FieldMask": "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"
        })
    
    print(req)
    etaResponse = req.json()
    print(etaResponse)
    
    return JsonResponse(req.json(), safe=False)