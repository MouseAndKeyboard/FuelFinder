mapboxgl.accessToken = 'pk.eyJ1Ijoic21vaGFuMjAwMSIsImEiOiJjbDVkaDZiNmwwNmwwM2ZvMXYwbDVieG9uIn0.hpEwFPqANepe3lUep9EU1Q';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/smohan2001/cl5dh88vv000o15pi194xhvy2', // style URL
    center: [115.816,-31.980], // starting position [lng, lat]
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
)

const direction = new MapboxDirections({
  accessToken: mapboxgl.accessToken,
  unit: 'metric',
  profile: 'mapbox/driving'
})

direction.on('route', (event) => console.log(event))

map.addControl(
  direction
);