<template>
  <div class="container mx-auto bg-green-100" style="width: 100%;">
    <AuthNavBar />
    <div class="flex">
      <SideBar />
      <FarmNameModal :visible="isModalVisible" @submit="handleModalSubmit" @cancel="handleModalCancel" />
      <div class="flex-1">
        <div class="relative">
          <div id="map" class="leaflet-container"
            style="height: 600px; width: 70%; border: 1rem solid green; margin: auto; margin-top: 15px;"></div>

          <div class="absolute top-2 right-2 flex flex-col space-y-2">
            <button @click="toggleLabels"
              class="bg-green-700 hover:bg-green-500 text-white px-4 py-2 rounded-md transition duration-200">Toggle
              Labels</button>
            <button v-if="polygonDrawn" @click="savePolygon"
              class="bg-green-700 hover:bg-green-500 text-white px-4 py-2 rounded-md transition duration-200">Save
              Polygon</button>
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
import FarmNameModal from '@/Components/FarmNameModal.vue';

const googleMapsKey = ''; // Your Google Maps API key
const showLabels = ref(true);
const polygonDrawn = ref(false);
const drawnCoordinates = ref(null);
const isModalVisible = ref(false);

let googleLayer = null;
let map;

const toggleLabels = () => {
  showLabels.value = !showLabels.value;
  if (googleLayer) {
    map.removeLayer(googleLayer);

    googleLayer = L.gridLayer.googleMutant({
      type: showLabels.value ? 'hybrid' : 'satellite',
      styles: showLabels.value ? defaultStyle : hideLabelsStyle,
      maxZoom: 18,
      key: googleMapsKey
    }).addTo(map);
  }
};

const defaultStyle = [];
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
    type: 'hybrid',
    styles: defaultStyle,
    maxZoom: 18,
    key: googleMapsKey
  }).addTo(map);

  const drawnItems = L.featureGroup().addTo(map);

  const drawControl = new L.Control.Draw({
    draw: {
      polyline: false,
      rectangle: false,
      circle: false,
      marker: false,
      circlemarker: false,
      polygon: true
    },
    edit: {
      featureGroup: drawnItems,
      edit: {
        selectedPathOptions: {
          maintainColor: true
        }
      },
      remove: {}
    }
  });

  map.addControl(drawControl);

  map.on(L.Draw.Event.CREATED, (event) => {
    const layer = event.layer;
    drawnItems.addLayer(layer);

    // Get the coordinates of the drawn polygon
    drawnCoordinates.value = layer.toGeoJSON().geometry.coordinates;
    polygonDrawn.value = true; // Enable the "Save Polygon" button
  });

  map.on(L.Draw.Event.DELETED, () => {
    // Handle the deletion of polygons
    polygonDrawn.value = false; // Disable the "Save Polygon" button
    drawnCoordinates.value = null; // Reset the coordinates
  });
});

const savePolygon = () => {
  if (drawnCoordinates.value) {
    isModalVisible.value = true;
  }
};

const handleModalSubmit = (farmName) => {
  if (drawnCoordinates.value) {
    axios.post('/api/farm-zone', {
      coordinates: drawnCoordinates.value,
      farm_name: farmName
    }, {
      withCredentials: true
    })
      .then(response => {
        console.log('Polygon saved:', response.data);
        polygonDrawn.value = false;
        drawnCoordinates.value = null;
        isModalVisible.value = false;
        alert('The farm zone is saved successfully!');
      })
      .catch(error => {
        alert('A problem has occurred, failed to save the farm zone!');
      });
  }
};

const handleModalCancel = () => {
  isModalVisible.value = false;
};

</script>

<style scoped>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 10;
}
</style>
