// If you're adding a number of markers, you may want to drop them on the map
// consecutively rather than all at once. This example shows how to use
// window.setTimeout() to space your markers' animation.


var optimizedRoute = '{"Truck0":[{"lat":24.50836693075162,"lng":54.40520005022369},{"lat":24.494844691128918,"lng":54.369475192138644},{"lat":24.48727875202071,"lng":54.3804539106812},{"lat":24.50836693075162,"lng":54.40520005022369}],"Truck1":[{"lat":24.50836693075162,"lng":54.40520005022369},{"lat":24.462770104509687,"lng":54.38993715541294},{"lat":24.466642137604556,"lng":54.32795364405558},{"lat":24.50836693075162,"lng":54.40520005022369}]}';
var tempData = JSON.parse(optimizedRoute);
var selectedLocation = [];
let markers = [];
let map;

const locations1 = [

    {
      lat: 24.50836693075162,
      lng: 54.40520005022369
  
    },
    {
      lat: 24.462770104509687,
      lng: 54.38993715541294
    }
  ]
  const locations2 = [
  
    {
      lat: 24.494844691128918,
      lng: 54.369475192138644
    },
    {
      lat: 24.48727875202071,
      lng: 54.3804539106812
    },
    {
      lat: 24.466642137604556,
      lng: 54.32795364405558
    }
  ]




  const start = [
  
    {
      lat: 24.52417785198881,
      lng: 54.43458798384425

     
    }];

function initMap() {

    map = new google.maps.Map(document.getElementById("googleMap"), {
        zoom: 12,
        center: { lat: 24.50, lng: 54.40 },
    });

    google.maps.event.addListener(map, 'click', function (event) {
        selectedLocation.push(event.latLng);
        
        addLocation(event.latLng);
        
        markers.push(new google.maps.Marker({
            position: event.latLng,
            map: map,
        }))
    });


    markers.push(
        new google.maps.Marker({
            position: position,
            map,
            animation: google.maps.Animation.DROP,
        })
    )

    var data2 = JSON.parse(optimizedRoute);
    console.log(data2.Truck0[0].lat);

    //========= Pin Drop =========================
    //document.getElementById("drop").addEventListener("click", drop);
    const image = 'warehouse.png';
    const beachMarker = new google.maps.Marker({
        position: { lat: 24.524090003437255, lng: 54.43451288218101 },
        map,
        icon: image,
    });
    //========= Pin Drop =========================

    //========= Route ============================
    // const directionsService = new google.maps.DirectionsService();
    // const directionsRenderer = new google.maps.DirectionsRenderer();
    // const directionsRenderer2 = new google.maps.DirectionsRenderer();
    // directionsRenderer.setMap(map);

    // directionsRenderer.setOptions({
    //     polylineOptions: {
    //         strokeColor: 'purple'
    //     }
    // });


    

    // directionsRenderer2.setOptions({
    //     polylineOptions: {
    //         strokeColor: 'green'
    //     }
    // });
   // calculateAndDisplayRoute(directionsService, directionsRenderer2);

    // directionsRenderer2.setMap(map);
    // document.getElementById("submit2").addEventListener("click", () => {
    //   calculateAndDisplayRoute2(directionsService, directionsRenderer2);
    // });

}

//========= Route ============================






//======================== Pin Drop ======================================================

function drop() {
    clearMarkers();

    
        addMarkerWithTimeout(start[0], 7 * 200);
    

    for (let i = 0; i < tempData.Truck0.length; i++) {
        addMarkerWithTimeout(tempData.Truck0[i], i * 200);
    }

    for (let i = 0; i < tempData.Truck1.length; i++) {
        addMarkerWithTimeout(tempData.Truck1[i], i * 200);
    }
}


function addMarkerWithTimeout(position, timeout) {
    window.setTimeout(() => {
        markers.push(
            new google.maps.Marker({
                position: position,
                map,
                animation: google.maps.Animation.DROP,
            })
        );
    }, timeout);
}

function clearMarkers() {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }

    markers = [];
}

//======================== Pin Drop ======================================================



//======================== Route Drawing =================================================


function calculateAndDisplayRoute(directionsService, directionsRenderer,r) {
    const waypts = [];
   

    var locArray = r
    

    console.log(locArray[0].lat);
    var start = new google.maps.LatLng(24.524090003437255, 54.43441632248009);
    var stop = new google.maps.LatLng(24.524090003437255, 54.43441632248009)

    for (let i = 0; i < locArray.length; i++) {

        var temp = new google.maps.LatLng(locArray[i].lat, locArray[i].lng)


        waypts.push({
            location: temp,
            stopover: true,
        });

    }


    directionsService
        .route({
            origin: start,
            destination: stop,
            waypoints: waypts,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.DRIVING,
        })
        .then((response) => {
            directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + status));
}


function calculateAndDisplayRoute2(directionsService, directionsRenderer,r) {
    const waypts = [];
    const locArray = r;
    var start = new google.maps.LatLng(24.524090003437255, 54.43441632248009);
    var stop = new google.maps.LatLng(24.524090003437255, 54.43441632248009)


    for (let i = 0; i < locArray.length; i++) {

        var temp = new google.maps.LatLng(locArray[i].lat, locArray[i].lng)


        waypts.push({
            location: temp,
            stopover: true,
        });

    }


    directionsService
        .route({
            origin: start,
            destination: stop,
            waypoints: waypts,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.DRIVING,
        })
        .then((response) => {
            directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + status));
}


//======================== Route Drawing =================================================



function getOptimizedRoute(listOfLocations) {

    setTimeout(2000);

    var yourUrl = '';
    var tempData = JSON.parse(optimizedRoute);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", yourUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    // xhr.setRequestHeader('Access-Control-Allow-Methods', 'POST');
    // xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    // xhr.setRequestHeader('Access-Control-Allow-Headers', 'Content-Type');

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    directionsRenderer.setOptions({
      polylineOptions: {
          strokeColor: 'purple'
      }
  });

  const directionsRenderer2 = new google.maps.DirectionsRenderer();
  directionsRenderer2.setMap(map);
  directionsRenderer2.setOptions({
    polylineOptions: {
        strokeColor: 'Green'
    }
});

    
    xhr.send(JSON.stringify({
        value: listOfLocations
    }));

    xhr.onload = function() {
        console.log("HELLO")
        console.log(this.responseText);
        console.log(tempData);
        //var data = JSON.parse(this.responseText);
        
        var r1 = tempData.Truck0;
        var r2 = tempData.Truck1;


        calculateAndDisplayRoute(directionsService, directionsRenderer,r1);

        calculateAndDisplayRoute2(directionsService, directionsRenderer2,r2);
  
        drop();


      }







}


function addLocation(locationName) {
    var geocoder = geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'latLng': locationName }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {

                var ul = document.getElementById("locationList");
                var li = document.createElement("li");
                li.appendChild(document.createTextNode(results[1].formatted_address));
                li.className = "list-group-item list-group-item-primary";
                ul.appendChild(li);

            }
        }
    });





}