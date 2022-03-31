// The Auth0 client, initialized in configureClient()
let auth0 = null;

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

    const response = await fetch("/api/external", {
      headers: {
        Authorization: `Bearer ${token}`
      },
      method: 'POST',
      body: JSON.stringify({
        position: [0, 0]
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

  if (isAuthenticated) {
    console.log("> User is authenticated");
    window.history.replaceState({}, document.title, window.location.pathname);
    updateUI();
    return;
  }

  console.log("> User not authenticated");

  const query = window.location.search;
  const shouldParseResult = query.includes("code=") && query.includes("state=");

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

  getLatitude(){
    return this.latitude;
  }

  getLongitude(){
    return this.longitude;
  }
}

var coordinates = [];
var markers = [];



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



// fetch marker coords from backend

// finish work on authentication

// validate coodrinates (ad)


//validate form responses 

var coords1 = [24.47, 54.36]
var coords2 = [24.46, 54.37]
var coords3 = [24.45, 54.39]
var coords4 = [24.67, 54.46]

var coordinates = [coords1, coords2, coords3, coords4]

//everything related to distance calculator

//this function needs to be called upon pressing the request button
function validateLoc(user_lat, user_long){
  //top left = 24.475137206036116, 54.34893416592737
  //bottom right = 24.46994245833937, 54.38484229259571
  if( user_lat < 24.475137206036116 || user_lat > 24.46994245833937 || user_long < 54.34893416592737 || user_long > 54.38484229259571){
   //print the alert
   alert('We currently don’t provide service in your location');
   //prevent the request button from working
  }
 }

function drawPath(cordinate1,cordinate2) {//function that draws paths between markers
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
function drawEntirePath(coordinates){
  for (let i = 0; i < coordinates.length-1; i++){
    drawPath(coordinates[i], coordinates[i+1])
  }
}

drawEntirePath(coordinates)

function distanceMatrix(coordinates) {
  var matrix = []
  //need length of passed array
  var nodesNum= coordinates.length;
  for (var i = 0; i < nodesNum;i++) { 
    matrix.push([])
    var row = matrix[i]
    for (var j=0; j<nodesNum; j++) {

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

  //validate email
  var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  emailInput.type = 'email';
  emailInput.required = true;

  if (!re.test(emailInput.value)){
    emailInput.style.color = "red";
  } else {
    emailInput.style.color = "black";
  }

  //validate number
  correct = true
  numbers = phoneNumberInput.value.trim().split(" ");

  console.log(numbers)

  if (numbers.length != 3){
    correct = false
  } else if (numbers[0] != "+971") {
    correct = false
  } else if (isNaN(numbers[1]) || numbers[1].length != 1 && numbers[1].length != 2) {
    correct = false
  } else if (isNaN(numbers[2]) || numbers[2].length != 7) {
    correct = false
  }
  phoneNumberInput.style.color = correct ? "black" : "red"
}

requestBtn.onclick = validateForm
