<template>
  <div class="container mx-auto bg-green-100" style="width: 100%;">
    <div class="flex flex-nowrap justify-between items-start py-4">
      <div class="flex-shrink-0 ml-4">
        <button
          class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200"
          @click="showNDVILayer">Show NDVI Layer</button>
      </div>

      <div class="w-1/2 mr-4">
        <div id="map" class="leaflet-container" style="height: 600px; border: 1rem solid green;"></div>
      </div>

      <div class="flex-shrink-0 w-1/4">
        <div class="bg-white p-4 rounded shadow-lg" v-if="ndviLayerVisible">
          <h3 class="font-bold mb-2">NDVI Legend</h3>
          <div class="flex items-center mb-2">
            <span class="w-6 h-6 bg-blue-500 inline-block"></span>
            <span class="ml-2">Low (-0.2 to 0.0)</span>
          </div>
          <div class="flex items-center mb-2">
            <span class="w-6 h-6 bg-cyan-500 inline-block"></span>
            <span class="ml-2">Moderate (0.0 to 0.2)</span>
          </div>
          <div class="flex items-center mb-2">
            <span class="w-6 h-6 bg-green-500 inline-block"></span>
            <span class="ml-2">Healthy (0.2 to 0.4)</span>
          </div>
          <div class="flex items-center mb-2">
            <span class="w-6 h-6 bg-yellow-500 inline-block"></span>
            <span class="ml-2">Very Healthy (0.4 to 0.6)</span>
          </div>
          <div class="flex items-center">
            <span class="w-6 h-6 bg-red-500 inline-block"></span>
            <span class="ml-2">Extremely Healthy (0.6 to 0.8)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.gridlayer.googlemutant';

const googleMapsKey = ''; // Your Google Maps API key
const map = ref(null);
const coordinates = ref([]);
const farmId = ref(null); // Ref to store the farm ID
const ndviLayer = ref(null); // Store NDVI layer reference
const ndviLayerVisible = ref(false); // Track if NDVI layer is visible

const getFarmIdFromUrl = () => {
  const url = new URL(window.location.href);
  return url.pathname.split('/').pop(); // Get the last part of the URL
};

const fetchFarmZoneData = async (id) => {
  try {
    const response = await axios.get(`/api/farm-zone/${id}`);
    const rawCoordinates = response.data.coordinates;

    // Convert coordinates to [latitude, longitude]
    coordinates.value = convertCoordinates(rawCoordinates);
    initializeMap();
  } catch (error) {
    console.error('Error fetching farm zone data:', error);
  }
};

const convertCoordinates = (coords) => {
  return coords[0].map(coord => [coord[1], coord[0]]);
};

const initializeMap = () => {
  if (map.value) {
    map.value.remove();
  }

  map.value = L.map('map', {
    center: [30.427755, -9.598107],
    zoom: 11,
    zoomControl: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    touchZoom: false,
    dragging: false
  });

  L.gridLayer.googleMutant({
    type: 'hybrid',
    maxZoom: 18,
    key: googleMapsKey
  }).addTo(map.value);

  if (coordinates.value && coordinates.value.length) {
    const polygon = L.polygon(coordinates.value, { color: 'red', fillOpacity: 0, weight: 3 }).addTo(map.value);
    map.value.fitBounds(polygon.getBounds());
  }
};

// Show NDVI Layer Button Handler
const showNDVILayer = async () => {
  try {
    const response = await axios.get(`/api/farm-zone/${farmId.value}/ndvi`);
    const ndviTileUrl = response.data.tileUrl;

    if (ndviLayer.value) {
      map.value.removeLayer(ndviLayer.value);
    }

    // Add NDVI layer to the map
    ndviLayer.value = L.tileLayer(ndviTileUrl, {
      opacity: 0.6,
      attribution: 'NDVI Layer'
    }).addTo(map.value);

    // Show the NDVI legend
    ndviLayerVisible.value = true;
  } catch (error) {
    console.error('Error fetching NDVI layer:', error);
  }
};

onMounted(() => {
  farmId.value = getFarmIdFromUrl();
  if (farmId.value) {
    fetchFarmZoneData(farmId.value);
  }
});
</script>

<style scoped>
.leaflet-container {
  height: 100%;
  width: 100%;
  z-index: 10;
}
</style>
