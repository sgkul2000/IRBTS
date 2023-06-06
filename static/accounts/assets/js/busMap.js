async function initMap() {
    
    var curLocation = null
    var curStop = null
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const bus_name = document.querySelector("#bus-name").innerHTML;
    const stops_resp = await fetch('http://localhost:8000/smartTracking/stops/', {
        method: "POST",
        body: JSON.stringify({bus_name})
    })
    const stops = await stops_resp.json();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: {lat: 12.2958, lng: 76.6394},
    });
    
    const infoWindow = new google.maps.InfoWindow();
    let socket = new WebSocket(`ws://127.0.0.1:8000/ws/track/${bus_name}/`);
    
    socket.onmessage = (e) => {
        curLocation = JSON.parse(e.data).location;
        curStop = JSON.parse(e.data).cur_stop;
        autocomplete(document.getElementById("inputETA"), stops.map((el) => el.stop_name).filter((el, ind) => ind > stops.findIndex((stop) => stop.stop_name === curStop)));
        infoWindow.setPosition(JSON.parse(e.data).location);
        infoWindow.setContent("Current Location.");
        infoWindow.open(map, new google.maps.Marker({
            map: map,
            position: JSON.parse(e.data).location,
            label: "*"
        }));
        console.log("Current location set")
    };
    
    // render directions
    directionsRenderer.setMap(map);
    
    directionsService.route(
        {
            origin: {
                lat: stops[0].lat,
                lng: stops[0].long
            },
            destination: {
                lat: stops[stops.length - 1].lat,
                lng: stops[stops.length - 1].long
            },
            waypoints: stops.slice(1, stops.length - 1).map(el => {
                return {location: new google.maps.LatLng(el.lat, el.long), stopover: true }
            }),
            // waypoints: [{ location: new google.maps.LatLng(12.299641, 76.642704), stopover: true }],
            // waypoints: [{ location: { 'lat': 12.2958104, 'lng': 76.6393805 }, stopover: true }],
            travelMode: google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
            if (status === "OK") {
                directionsRenderer.setDirections(response);
            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );
    const format = (n) => {
        return (~~n).toString().padStart(2, '0')
    }
    document.getElementById("etaBtn").addEventListener("click", async () => {
        const eta_resp = await fetch('http://localhost:8000/smartTracking/get-eta/', {
        method: "POST",
        body: JSON.stringify({"stop": stops.find((el) => el.stop_name === document.getElementById("inputETA").value), "cur_location" :curLocation})
    })
    const eta = await eta_resp.json();
    duration = 
    seconds = parseInt(eta.routes[0].duration.slice(0,-1))
    // ':'.join([str(int(s/60/60 % 60)), str(int(s/60 % 60)), str(int(s%60))])
    document.getElementById("eta-result").innerHTML = "Expected ETA is: "+[format(seconds / 60 / 60),
    format(seconds / 60 % 60),
    format(seconds % 60)].join(':')

    })
}