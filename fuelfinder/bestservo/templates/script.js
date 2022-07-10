mapboxgl.accessToken = 'pk.eyJ1Ijoic21vaGFuMjAwMSIsImEiOiJjbDVkaDZiNmwwNmwwM2ZvMXYwbDVieG9uIn0.hpEwFPqANepe3lUep9EU1Q';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/smohan2001/cl5dh88vv000o15pi194xhvy2', // style URL
  center: [115.816, -31.980], // starting position [lng, lat]
  zoom: 13 // starting zoom
});

map.on('style.load', () => {
  map.setFog({}); // Set the default atmosphere style
});

map.addControl(
  new mapboxgl.GeolocateControl({
    positionOptions: {
      enableHighAccuracy: true
    },
    trackUserLocation: true,
    showUserHeading: true,
  }),
  'bottom-right'
);

const direction = new MapboxDirections({
  accessToken: mapboxgl.accessToken,
  unit: 'metric',
  profile: 'mapbox/driving',
});

direction.on('route', (event) => {
  var pointsArr = []
  allSteps = event.route[0].legs[0].steps
  stepsLen = event.route[0].legs[0].steps.length

  for (let i = 0; i < stepsLen; i++) {
    intersectionLen = allSteps[i].intersections.length
    intersections = allSteps[i].intersections
    for (let j = 0; j < intersectionLen; j++) {
      pointsArr.push([intersections[j].location[1], intersections[j].location[0]])
    }
  }
  // Need to send pointsArr to backend
  console.log(pointsArr)
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:8000/servo", true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    path: pointsArr,
    efficiency: 5,
    capacity: 50,
    current_tank: 2,
    RAC: 0,
    Woolies: 0
  }));
  xhr.onload = function () {
    console.log("HELLO")
    console.log(this.responseText);
    var data = JSON.parse(this.responseText);
    console.log(data);
  }
});

map.addControl(
  direction
);

/* direction.addWaypoint (
  1, [lng, lat]
); */
