<template>
  <div class="container mx-auto" style="width: 100%;">
    <AuthNavBar />
    <div class="flex">
      <SideBar />
      <div class="flex-1">
        <div class="relative">
          <div id="map" class="leaflet-container"
            style="height: 600px; width: 70%; border: 1rem solid green; margin: auto; margin-top: 15px;"></div>

          <!-- Button Container for Labels and Save -->
          <div class="absolute top-2 right-2 flex flex-col space-y-2">
            <!-- Toggle Button for Labels -->
            <button @click="toggleLabels" class="bg-green-700 hover:bg-green-500 text-white px-4 py-2 rounded-md transition duration-200">
              Toggle Labels
            </button>

            <!-- Save Polygon Button -->
            <button v-if="polygonDrawn" @click="savePolygon" class="bg-green-700 hover:bg-green-500 text-white px-4 py-2 rounded-md transition duration-200">
              Save Polygon
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import 'leaflet-draw';
import 'leaflet.gridlayer.googlemutant';
import AuthNavBar from '@/Components/AuthNavBar.vue';
import SideBar from '@/Components/SideBar.vue';
import axios from 'axios';

const googleMapsKey = ''; // Your Google Maps API key
const showLabels = ref(true); // Data property to toggle labels visibility
const polygonDrawn = ref(false); // Flag to track if a polygon is drawn
const drawnCoordinates = ref(null); // Stores the drawn polygon coordinates

let googleLayer = null;
let map;

const toggleLabels = () => {
  showLabels.value = !showLabels.value;
  if (googleLayer) {
    map.removeLayer(googleLayer); // Remove the current layer

    googleLayer = L.gridLayer.googleMutant({
      type: showLabels.value ? 'hybrid' : 'satellite', // Use 'hybrid' for labels, 'satellite' without labels
      styles: showLabels.value ? defaultStyle : hideLabelsStyle,
      maxZoom: 18,
      key: googleMapsKey
    }).addTo(map);
  }
};

const defaultStyle = []; // Default Google Maps style (no customizations)

const hideLabelsStyle = [
  {
    featureType: 'all',
    elementType: 'labels',
    stylers: [{ visibility: 'off' }]
  }
];

onMounted(() => {
  map = L.map('map').setView([30.427755, -9.598107], 11);

  if (!L.gridLayer.googleMutant) {
    console.error('GoogleMutant plugin not loaded');
    return;
  }

  googleLayer = L.gridLayer.googleMutant({
    type: 'hybrid', // I'm using 'hybrid' initially
    styles: defaultStyle,
    maxZoom: 18,
    key: googleMapsKey
  }).addTo(map);

  const drawnItems = L.featureGroup().addTo(map);

  const drawControl = new L.Control.Draw({
    edit: {
      featureGroup: drawnItems
    }
  });
  map.addControl(drawControl);

  map.on(L.Draw.Event.CREATED, (event) => {
    const layer = event.layer;
    drawnItems.addLayer(layer);

    // Get the coordinates of the drawn polygon
    drawnCoordinates.value = layer.toGeoJSON().geometry.coordinates;
    polygonDrawn.value = true; // Enable the "Save Polygon" button
    console.log('Polygon coordinates:', drawnCoordinates.value);
  });
});

const savePolygon = () => {
  if (drawnCoordinates.value) {
    axios.post('/api/save-farm-zone', {
      coordinates: drawnCoordinates.value
    }, {
      withCredentials: true
    })
    .then(response => {
      console.log('Polygon saved:', response.data);
      polygonDrawn.value = false; // Disable the "Save Polygon" button after saving
      drawnCoordinates.value = null; // Reset the coordinates
      alert('Polygon saved successfully!');
    })
    .catch(error => {
      console.error('Error saving polygon:', error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log('Error response data:', error.response.data);
        console.log('Error response status:', error.response.status);
        console.log('Error response headers:', error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log('Error request data:', error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error message:', error.message);
      }
      alert('Failed to save the polygon! Check the console for more details.');
    });
  }
};

</script>

<style scoped>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 10;
}
</style>
