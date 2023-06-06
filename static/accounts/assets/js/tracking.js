window.onload = () => {

    const dNameInput = document.getElementById('driverName');
    const dPhoneInput = document.getElementById('driverPhone');
    const bNoInput = document.getElementById('busNo');
    const startBtn = document.getElementById('startBtn')
    startBtn.addEventListener("click", async () => {
        
        // get location access
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                let socket = new WebSocket(`ws://127.0.0.1:8000/ws/track/${bNoInput.value}/`);

                socket.onopen = (e) => {
                    console.log("Connection established")
                    setInterval(() => {
                        console.log("Emmiting data")
                        socket.send(JSON.stringify({
                            'type': 'driver',
                            'driverName': dNameInput.value,
                            'driverPhone': dPhoneInput.value,
                            'busNo': bNoInput.value,
                            'location': {
                                'lat': position.coords.latitude,
                                'lng': position.coords.longitude,
                            },
                        }));
                    }, 3000)
                };


            }, (error) => {
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        alert("Please provide access to location")
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Location information is unavailable.")
                        break;
                    case error.TIMEOUT:
                        alert("Request timed out.")
                        break;
                    case error.UNKNOWN_ERROR:
                        alert("An unknown error occurred.")
                        break;
                }
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }


    });
    
}