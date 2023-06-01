async function initMap() {
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
}