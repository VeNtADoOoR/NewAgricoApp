<template>
    <div class="container mx-auto bg-green-100" style="width: 100%;">
      <div class="flex">
        <div class="flex-1">
          <div class="relative">
            <button
              class="bg-green-700 text-white px-4 py-2 rounded mt-4 hover:bg-green-500 transition duration-200"
              @click="showNDVILayer">Show NDVI Layer</button>
            <div id="map" class="leaflet-container"
              style="height: 600px; width: 70%; border: 1rem solid green; margin: auto; margin-top: 15px;">
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
      const polygon = L.polygon(coordinates.value, { color: 'red', fillOpacity: 0 , weight: 3}).addTo(map.value);
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
  