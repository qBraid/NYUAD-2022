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

var coords1 = [24.46, 54.37]
var coords2 = [24.46, 54.37]
var coords3 = [24.45, 54.39]

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



async function getLocation() {
    navigator.geolocation.getCurrentPosition(position => {
    const { latitude, longitude } = position.coords;
    console.log(latitude, longitude)
    return new Coordinate(latitude, longitude)
  }); 
}


async function addCoordinates(coordinates){

  coordinate = await getLocation();
  coordinates.push([coordinate.getLatitude(), coordinate.getLongitude()])

  // console.log(array[0].getLatitude(), array[0].getLongitude)
  
  // for(let i = 0; i < array.length; i++){
  //   L.marker(array[i]).addTo(map)
  //   console.log("array[0] has been marked.")
  // }
  // L.marker([coordinate.getLatitude(), coordinate.getLongitude()]).addTo(map)

  console.log("random")

}

setTimeout(addCoordinates(coordinates, map), 10000)


// //function to add marker
// function addMarker(coord, map){
//   var marker = L.marker(coord).addTo(map);
//   markers.push(marker);
//   marker.dragging.disable();
// }

// console.log()

// console.log(coordinates[0]);


coordinates.forEach((x) => markers.push(L.narker(x.addTo(map))));



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

// create a function to add a marker 

// fetch marker coords from backend

// finish work on authentication

// add a function that draws paths between markers 

// add a buntton in the ui that gets the location and console log

// validate coodrinates (ad)



//validate form responses


//email
var emailInput = document.getElementById('emailInput');
var phoneNumberInput = document.getElementById('phoneNumberInput');
var requestBtn = document.getElementById('call-api')

function checkNumber(value){

}


function validateForm(value) {


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

requestBtn.onclick = validateForm;