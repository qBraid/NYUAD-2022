// The Auth0 client, initialized in configureClient()
let auth0 = null;
let graph = []
let markers = []

/**
 * Starts the authentication flow
 */
const login = async (targetUrl) => {
  try {
    console.log("Logging in", targetUrl);

    const options = {
      redirect_uri: window.location.origin
    };

    if (targetUrl) {
      options.appState = { targetUrl };
    }

    await auth0.loginWithRedirect(options);
  } catch (err) {
    console.log("Log in failed", err);
  }
};

/**
 * Executes the logout flow
 */
const logout = () => {
  try {
    console.log("Logging out");
    auth0.logout({
      returnTo: window.location.origin
    });
  } catch (err) {
    console.log("Log out failed", err);
  }
};

/**
 * Retrieves the auth configuration from the server
 */
const fetchAuthConfig = () => fetch("/auth_config.json");

/**
 * Initializes the Auth0 client
 */
const configureClient = async () => {
  const response = await fetchAuthConfig();
  const config = await response.json();

  auth0 = await createAuth0Client({
    domain: config.domain,
    client_id: config.clientId,
    audience: config.audience
  });
};

/**
 * Checks to see if the user is authenticated. If so, `fn` is executed. Otherwise, the user
 * is prompted to log in
 * @param {*} fn The function to execute if the user is logged in
 */
const requireAuth = async (fn, targetUrl) => {
  const isAuthenticated = await auth0.isAuthenticated();

  if (isAuthenticated) {
    return fn();
  }

  return login(targetUrl);
};

/**
 * Calls the API endpoint with an authorization token
 */
const callApi = async () => {
  try {
    const token = await auth0.getTokenSilently();

    console.log(graph)
    await insertSelfNode();
    console.log(graph)
    await fetch("http://localhost:3000/api/graph", {
      headers: {
        Authorization: `Bearer ${token}`
      },
      method: 'POST',
      body: JSON.stringify({
        graph
      })
    })

    const pathData = await fetch("http://localhost:3000/api/path", {
      headers: {
        Authorization: `Bearer ${token}`
      },
      method: 'GET'
    })
    const path = await pathData.json()
    let path_to_markers = []
    for (let i = 0; i < path.path.length; i++) {
      path_to_markers.push(markers[path.path[i]])
    }
    drawEntirePath(path_to_markers)

    const response = await fetch("/api/external", {
      headers: {
        Authorization: `Bearer ${token}`
      },
      method: 'POST',
      body: JSON.stringify({
        position: position
      })
    });

    const responseData = await response.json();
    const responseElement = document.getElementById("api-call-result");

    responseElement.innerText = JSON.stringify(responseData, {}, 2);

    document.querySelectorAll("pre code").forEach(hljs.highlightBlock);

    eachElement(".result-block", (c) => c.classList.add("show"));
  } catch (e) {
    console.error(e);
  }
};

// Will run when page finishes loading
window.onload = async () => {
  await configureClient();
  const location = await getPosition();
  console.log(location)
  L.marker(location).addTo(map)


  // If unable to parse the history hash, default to the root URL
  if (!showContentFromUrl(window.location.pathname)) {
    showContentFromUrl("/");
    window.history.replaceState({ url: "/" }, {}, "/");
  }

  const bodyElement = document.getElementsByTagName("body")[0];

  // Listen out for clicks on any hyperlink that navigates to a #/ URL
  bodyElement.addEventListener("click", (e) => {
    if (isRouteLink(e.target)) {
      const url = e.target.getAttribute("href");

      if (showContentFromUrl(url)) {
        e.preventDefault();
        window.history.pushState({ url }, {}, url);
      }
    } else if (e.target.getAttribute("id") === "call-api") {
      e.preventDefault();
      callApi();
    }
  });

  const isAuthenticated = await auth0.isAuthenticated();
  const token = await auth0.getTokenSilently();


  if (isAuthenticated) {
    console.log("> User is authenticated");
    window.history.replaceState({}, document.title, window.location.pathname);
    updateUI();
  }

  console.log("> User not authenticated");

  const query = window.location.search;
  const shouldParseResult = query.includes("code=") && query.includes("state=");
  console.log("is this working")
  if (shouldParseResult) {
    console.log("> Parsing redirect");
    try {
      const result = await auth0.handleRedirectCallback();

      if (result.appState && result.appState.targetUrl) {
        showContentFromUrl(result.appState.targetUrl);
      }

      console.log("Logged in!");
    } catch (err) {
      console.log("Error parsing redirect:", err);
    }

    window.history.replaceState({}, document.title, "/");
  }

  const graphData = await fetch("http://localhost:3000/api/graph", {
    headers: {
      Authorization: `Bearer ${token}`
    },
    method: 'GET'
  })
  const graphObj = await graphData.json()
  graph = graphObj.graph
  console.log(graphObj)

  const markerData = await fetch("http://localhost:3000/api/markers", {
    headers: {
      Authorization: `Bearer ${token}`
    },
    method: 'GET'
  })
  const markerObj = await markerData.json()
  markers = markerObj.markers
  console.log(graphObj)

  const pathData = await fetch("http://localhost:3000/api/path", {
    headers: {
      Authorization: `Bearer ${token}`
    },
    method: 'GET'
  })
  const pathObj = await pathData.json()
  const path = pathObj.path

  // drawMarkers(markersObj)

  // let actualMarkers = []


  let actualMarkers = []
  console.log(path)
  console.log(markers)


  for (let i = 0; i < path[0].length; i++) {
    actualMarkers.push(markers[path[0][i]])
    console.log(path[0][i])
  }

  console.log(actualMarkers)
  // draw markers
  drawEntirePath(actualMarkers)


  updateUI();
};



// maps

var map = L.map('map').setView([24.47, 54.36], 12.5);


var token = "pk.eyJ1IjoiaGFtemFib3Vkb3VjaGUiLCJhIjoiY2wxZGk1MHo3MGhucjNibnJ2bjl6NTZ4dCJ9.IJQwmeYtLKNG_Cl_IqjkXw"

L.tileLayer(`https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=${token}`, {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'your.mapbox.access.token'
}).addTo(map);

// var coords1 = [24.46, 54.37]
// var coords2 = [24.46, 54.37]
// var coords3 = [24.45, 54.39]

class Coordinate {

  constructor(latitude, longitude) {
    this.latitude = latitude;
    this.longitude = longitude;
  }

  getLatitude() {
    return this.latitude;
  }

  getLongitude() {
    return this.longitude;
  }
}

var coordinates = [];
var buses = [[24.474, 54.368]];



// async function getLocation() {
//     navigator.geolocation.getCurrentPosition(position => {
//     const { latitude, longitude } = position.coords;
//     console.log(latitude, longitude)
//     return new Coordinate(latitude, longitude)
//   }); 
// }


// async function addCoordinates(coordinates){

//   coordinate = await getLocation();
//   coordinates.push([coordinate.getLatitude(), coordinate.getLongitude()])

// console.log(array[0].getLatitude(), array[0].getLongitude)

// for(let i = 0; i < array.length; i++){
//   L.marker(array[i]).addTo(map)
//   console.log("array[0] has been marked.")
// }
// L.marker([coordinate.getLatitude(), coordinate.getLongitude()]).addTo(map)

// console.log("random")

// }

// setTimeout(addCoordinates(coordinates, map), 1)


// //function to add marker
// function addMarker(coord, map){
//   var marker = L.marker(coord).addTo(map);
//   markers.push(marker);
//   marker.dragging.disable();
// }

// console.log()

// console.log(coordinates[0]);


// coordinates.forEach((x) => markers.push(L.narker(x.addTo(map))));



// var coords1 = [24.7, 24.9]
// var coords2 = [24.46, 54.37]
// var coords3 = [24.45, 54.39]

// var marker1 = L.marker(coords1).addTo(map);
// var marker2 = L.marker(coords2).addTo(map);
// var marker2 = L.marker(coords3).addTo(map);




// L.Routing.control({
//   waypoints: [
//     L.latLng(coords1[0], coords1[1]),
//     L.latLng(coords2[0], coords2[1])
//   ],
//   color: "blue",
//   lineOptions: { styles: [{ color: '#242c81', weight: 2 }] },
//   draggableWaypoints: false,
// }).addTo(map);


// L.Routing.control({
//   waypoints: [
//     L.latLng(coords3[0], coords3[1]),
//     L.latLng(coords2[0], coords2[1])
//   ],
//   lineOptions: { styles: [{ color: '#242c81', weight: 2 }] },
//   draggableWaypoints: false,
// }).addTo(map);

// fetch("http://localhost:3010/api/private").then((res) => res.json()).then((data) => { console.log(data) })


// organise our code here

// FIXME: fetch this from backend
let buses = []


// fetch marker coords from backend

// finish work on authentication

// validate coodrinates (ad)


//validate form responses 

var coords1 = [24.47, 54.36]
var coords2 = [24.46, 54.37]
var coords3 = [24.45, 54.39]
var coords4 = [24.47, 54.3766]

var coordinates = [coords1, coords2, coords3, coords4]

//everything related to distance calculator

//this function needs to be called upon pressing the request button
function validateLoc(user_lat, user_long) {
  //top left = 24.475137206036116, 54.34893416592737
  //bottom right = 24.46994245833937, 54.38484229259571
  if (user_lat < 24.475137206036116 || user_lat > 24.46994245833937 || user_long < 54.34893416592737 || user_long > 54.38484229259571) {
    //print the alert
    alert('We currently don’t provide service in your location');
    //prevent the request button from working
  }
}

var LeafIcon = L.Icon.extend({
  options: {
    iconSize: [50, 50],
    shadowSize: [0, 0],
    //  iconAnchor:   [22, 94],
    //  shadowAnchor: [4, 62],
    //  popupAnchor:  [-3, -76]
  }
});

var busIcon = new LeafIcon({
  iconUrl: '../images/ambulance.png',
  shadowUrl: '../images/ambulance.png'
})

function drawBuses(buses) {
  for (let i = 0; i < buses.length; i++) {
    L.marker(buses[i], {
      icon: busIcon,
      color: "red",
      fillColor: "#f03",
      fillOpacity: 0.5,
      radius: 30
    }).addTo(map);
  }
}

function drawPath(cordinate1, cordinate2) {//function that draws paths between markers
  L.Routing.control({
    waypoints: [
      L.latLng(cordinate1[0], cordinate1[1]),
      L.latLng(cordinate2[0], cordinate2[1])
    ],
    lineOptions: { styles: [{ color: '#242C81', weight: 2 }] },
    draggableWaypoints: false,
    show: false //shows information for the route
  }).addTo(map);
}

//function that draws the entire path
function drawEntirePath(coordinates) {
  for (let i = 0; i < coordinates.length - 1; i++) {
    drawPath(coordinates[i], coordinates[i + 1])
  }
}

function drawEverything(coordinates) {
  drawEntirePath(coordinates)
  drawBuses(buses)
}

drawEverything(coordinates)

function distanceMatrix(coordinates) {
  var matrix = []
  //need length of passed array
  var nodesNum = coordinates.length;
  for (var i = 0; i < nodesNum; i++) {
    matrix.push([])
    var row = matrix[i]
    for (var j = 0; j < nodesNum; j++) {

      var fromMarker = L.latLng(coordinates[i]);
      var toMarker = L.latLng(coordinates[j]);

      var distance = fromMarker.distanceTo(toMarker);
      matrix[i].push(distance)
      // console.log(data);
    }
  }
  console.log(matrix)
}

console.log("hey!")
distanceMatrix(coordinates)


//email
var emailInput = document.getElementById('emailInput');
var phoneNumberInput = document.getElementById('phoneNumberInput');
var requestBtn = document.getElementById('call-api')

function validateForm() {

  let correct = true
  //validate email
  var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  emailInput.type = 'email';
  emailInput.required = true;

  if (!re.test(emailInput.value)) {
    correct = false;
    emailInput.style.color = "red";
  } else {
    emailInput.style.color = "black";
  }

  //validate number
  numbers = phoneNumberInput.value.trim().split(" ");

  console.log(numbers)

  if (numbers.length != 3) {
    correct = false
  } else if (numbers[0] != "+971") {
    correct = false
  } else if (isNaN(numbers[1]) || numbers[1].length != 1 && numbers[1].length != 2) {
    correct = false
  } else if (isNaN(numbers[2]) || numbers[2].length != 7) {
    correct = false
  }
  phoneNumberInput.style.color = correct ? "black" : "red"
  return correct
}

requestBtn.onclick = validateForm


function getPositionWrapped(options) {
  return new Promise((resolve, reject) =>
    navigator.geolocation.getCurrentPosition(resolve, reject, options)
  );
}

const getPosition = async () => {
  const location = await getPositionWrapped({});
  return [location.coords.latitude, location.coords.longitude]
}

// insert new node in the graph
const insertSelfNode = async () => {
  const token = await auth0.getTokenSilently();
  const location = await getPosition()

  const newNodeNumber = markers.length;

  for (let i = 0; i < newNodeNumber; i++) {
    let distance = await calculateDistance(markers[i], location);
    graph.push([i, newNodeNumber, { weight: distance }]);
  }
  // update graph on backend
  console.log(graph)
  await fetch("http://localhost:3000/api/graph", {
    headers: {
      Authorization: `Bearer ${token}`
    },
    method: 'POST',
    body: JSON.stringify({
      graph
    })
  });

  markers.push(location)
  // update markers on backend
  await fetch("http://localhost:3000/api/markers", {
    headers: {
      Authorization: `Bearer ${token}`
    },
    method: 'POST',
    body: JSON.stringify({
      markers
    })
  });
}

async function calculateDistance(pos1, pos2) {
  var wayPoint1 = L.latLng(pos1[0], pos1[1]);
  var wayPoint2 = L.latLng(pos2[0], pos2[1]);
  rWP1 = new L.Routing.Waypoint;
  rWP1.latLng = wayPoint1;
  rWP2 = new L.Routing.Waypoint;
  rWP2.latLng = wayPoint2;
  var d = 0
  var myRoute = L.Routing.osrmv1();

  const wrapperPromise = (r1, r2) => {
    return new Promise((resolve, reject) => {
      myRoute.route([r1, r2], function (err, routes) {
        d = routes[0].summary.totalDistance;
        resolve(d)
      });
    })
  }
  d = await wrapperPromise(rWP1, rWP2)
  return d
}

// (async () => {
//   console.log(await calculateDistance([21.41, 52.04], [21.11, 52.4]));
// })();

function drawMarkers(markers) {
  console.log("drawing markers")
  for (let i = 0; i < markers.length; i++) {
    L.marker(markers[i]).addTo(map);
  }

  let data = await response.json()
  return data
}



function refreshPage() {
  window.location.reload();
}
