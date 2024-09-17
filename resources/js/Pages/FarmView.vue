<template>
  <div class="container mx-auto bg-green-100" style="width: 100%;">
    <div class="flex flex-nowrap justify-between items-start py-4">
      <div class="flex flex-col ml-4">
        <button class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mb-2"
          @click="showNDVILayer" :disabled="NdviLoading">
          <span v-if="NdviLoading"
            class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-t-transparent rounded-full"></span>
          <span v-if="!NdviLoading">Show NDVI Layer</span>
        </button>
        <button class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 my-2"
          @click="showEVILayer" :disabled="EviLoading">
          <span v-if="EviLoading"
            class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-t-transparent rounded-full"></span>
          <span v-if="!EviLoading">Show EVI Layer</span>
        </button>
        <button class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 my-2"
          @click="showNDWILayer" :disabled="NdwiLoading">
          <span v-if="NdwiLoading"
            class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-t-transparent rounded-full"></span>
          <span v-if="!NdwiLoading">Show NDWI Layer</span>
        </button>
      </div>

      <div class="w-1/2 mr-4">
        <div id="map" class="leaflet-container" style="height: 600px; border: 1rem solid green;"></div>
      </div>

      <!-- Legend Container -->
      <div class="flex-shrink-0 w-1/4">
        <div class="bg-white p-4 rounded shadow-lg" v-if="ndviLayerVisible || eviLayerVisible || ndwiLayerVisible">
          <h3 class="font-bold mb-2" v-if="ndviLayerVisible">NDVI Legend</h3>
          <h3 class="font-bold mb-2" v-if="eviLayerVisible">EVI Legend</h3>
          <h3 class="font-bold mb-2" v-if="ndwiLayerVisible">NDWI Legend</h3>

          <!-- NDVI Legend -->
          <div v-if="ndviLayerVisible">
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-blue-500 inline-block"></span>
              <span class="ml-2">Low</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-cyan-500 inline-block"></span>
              <span class="ml-2">Moderate</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-green-500 inline-block"></span>
              <span class="ml-2">Healthy</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-yellow-500 inline-block"></span>
              <span class="ml-2">Very Healthy</span>
            </div>
            <div class="flex items-center">
              <span class="w-6 h-6 bg-red-500 inline-block"></span>
              <span class="ml-2">Extremely Healthy</span>
            </div>
          </div>

          <!-- EVI Legend -->
          <div v-if="eviLayerVisible">
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-blue-500 inline-block"></span>
              <span class="ml-2">Low Vegetation</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-white inline-block"></span>
              <span class="ml-2">Moderate Vegetation</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-green-500 inline-block"></span>
              <span class="ml-2">High Vegetation</span>
            </div>
          </div>

          <!-- NDWI Legend -->
          <div v-if="ndwiLayerVisible">
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-orange-900 inline-block"></span>
              <span class="ml-2">Low Water</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-white inline-block"></span>
              <span class="ml-2">Moderate Water</span>
            </div>
            <div class="flex items-center mb-2">
              <span class="w-6 h-6 bg-blue-500 inline-block"></span>
              <span class="ml-2">High Water</span>
            </div>
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
const eviLayer = ref(null); // Store EVI layer reference
const ndwiLayer = ref(null); // Store NDWI layer reference
const ndviLayerVisible = ref(false); // Track if NDVI layer is visible
const eviLayerVisible = ref(false);
const ndwiLayerVisible = ref(false); // Track if NDWI layer is visible
const NdviLoading = ref(false); // Track NDVI loading state
const EviLoading = ref(false); // Track EVI loading state
const NdwiLoading = ref(false); // Track NDWI loading state

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
    type: 'satellite',
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
  NdviLoading.value = true; // Start loading
  try {
    const response = await axios.get(`/api/farm-zone/${farmId.value}/ndvi`);
    const ndviTileUrl = response.data.tileUrl;

    // Remove existing layers if any
    if (ndviLayer.value) {
      map.value.removeLayer(ndviLayer.value);
    }
    if (eviLayer.value) {
      map.value.removeLayer(eviLayer.value);
      eviLayerVisible.value = false; // Hide EVI layer legend
    }
    if (ndwiLayer.value) {
      map.value.removeLayer(ndwiLayer.value);
      ndwiLayerVisible.value = false; // Hide NDWI layer legend
    }

    // Add NDVI layer to the map
    ndviLayer.value = L.tileLayer(ndviTileUrl, {
      opacity: 0.8,
      attribution: 'NDVI Layer'
    }).addTo(map.value);

    ndviLayerVisible.value = true; // Show NDVI layer legend
  } catch (error) {
    console.error('Error fetching NDVI layer:', error);
  } finally {
    NdviLoading.value = false; // End loading
  }
};

// Show EVI Layer Button Handler
const showEVILayer = async () => {
  EviLoading.value = true; // Start loading
  try {
    const response = await axios.get(`/api/farm-zone/${farmId.value}/evi`);
    const eviTileUrl = response.data.tileUrl;

    // Remove existing layers if any
    if (ndviLayer.value) {
      map.value.removeLayer(ndviLayer.value);
      ndviLayerVisible.value = false; // Hide NDVI layer legend
    }
    if (eviLayer.value) {
      map.value.removeLayer(eviLayer.value);
    }
    if (ndwiLayer.value) {
      map.value.removeLayer(ndwiLayer.value);
      ndwiLayerVisible.value = false; // Hide NDWI layer legend
    }

    // Add EVI layer to the map
    eviLayer.value = L.tileLayer(eviTileUrl, {
      opacity: 0.8,
      attribution: 'EVI Layer'
    }).addTo(map.value);

    eviLayerVisible.value = true; // Show EVI layer legend
  } catch (error) {
    console.error('Error fetching EVI layer:', error);
  } finally {
    EviLoading.value = false; // End loading
  }
};

// Show NDWI Layer Button Handler
const showNDWILayer = async () => {
  NdwiLoading.value = true; // Start loading
  try {
    const response = await axios.get(`/api/farm-zone/${farmId.value}/ndwi`);
    const ndwiTileUrl = response.data.tileUrl;

    // Remove existing layers if any
    if (ndviLayer.value) {
      map.value.removeLayer(ndviLayer.value);
      ndviLayerVisible.value = false; // Hide NDVI layer legend
    }
    if (eviLayer.value) {
      map.value.removeLayer(eviLayer.value);
      eviLayerVisible.value = false; // Hide EVI layer legend
    }
    if (ndwiLayer.value) {
      map.value.removeLayer(ndwiLayer.value);
    }

    // Add NDWI layer to the map
    ndwiLayer.value = L.tileLayer(ndwiTileUrl, {
      opacity: 0.8,
      attribution: 'NDWI Layer'
    }).addTo(map.value);

    ndwiLayerVisible.value = true; // Show NDWI layer legend
  } catch (error) {
    console.error('Error fetching NDWI layer:', error);
  } finally {
    NdwiLoading.value = false; // End loading
  }
};

onMounted(() => {
  farmId.value = getFarmIdFromUrl();
  fetchFarmZoneData(farmId.value);
});
</script>


<style scoped>
.spinner-border {
  border-width: 0.2em;
  border-color: rgba(0, 0, 0, 0.1);
}
</style>
