<template>
  <div class="container mx-auto" style="width: 100%;">
    <AuthNavBar />
    <div class="flex">
      <SideBar />
      <div class="flex-1">
        <div class="relative">
          <div id="map" class="leaflet-container"
            style="height: 600px; width: 70%; border: 1rem solid green; margin: auto; margin-top: 15px;"></div>

          <!-- Toggle Button for Labels -->
          <button @click="toggleLabels" class="absolute top-2 right-2 bg-green-500 text-white px-4 py-2 rounded-md">
            Toggle Labels
          </button>
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

let googleLayer = null;

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

let map;

onMounted(() => {
  map = L.map('map').setView([30.427755, -9.598107], 11);

  if (!L.gridLayer.googleMutant) {
    console.error('GoogleMutant plugin not loaded');
    return;
  }

  googleLayer = L.gridLayer.googleMutant({
    type: 'hybrid', // Im using 'hybrid' initially
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
    const coordinates = layer.toGeoJSON().geometry.coordinates;
    console.log('Polygon coordinates:', coordinates);

    // Send the coordinates to the backend
    savePolygon(coordinates);
  });

  const savePolygon = (coordinates) => {
    axios.post('/api/save-farm-zone', {
      coordinates: coordinates
    })
      .then(response => {
        console.log('Polygon saved:', response.data);
        // You can handle success feedback to the user here
      })
      .catch(error => {
        console.error('Error saving polygon:', error);
        // You can handle error feedback to the user here
      });
  };
});
</script>

<style scoped>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 10;
}
</style>
