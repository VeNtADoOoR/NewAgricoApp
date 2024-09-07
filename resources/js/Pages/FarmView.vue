<template>
    <div class="container mx-auto bg-green-100" style="width: 100%;">
        <div class="flex">
            <div class="flex-1">
                <div class="relative">
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

const googleMapsKey = '';

const map = ref(null);
const coordinates = ref([]);

// Extract the farm ID from the URL
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
        console.log('Converted Coordinates:', coordinates.value); // Debug log

        // Initialize the map with the fetched coordinates
        initializeMap();
    } catch (error) {
        console.error('Error fetching farm zone data:', error);
    }
};

// Helper function to convert coordinates from [longitude, latitude] to [latitude, longitude]
const convertCoordinates = (coords) => {
    // Flatten the coordinates and convert each pair
    return coords[0].map(coord => [coord[1], coord[0]]);
};

const initializeMap = () => {
    if (map.value) {
        // Clear the existing map if any
        map.value.remove();
    }

    map.value = L.map('map', {
        center: [30.427755, -9.598107],
        zoom: 11,
        zoomControl: false, // Disable zoom controls
        scrollWheelZoom: true, // Disable zooming with the scroll wheel
        doubleClickZoom: false, // Disable zooming with double click
        touchZoom: false, // Disable touch zooming on mobile devices
        dragging: false // Optionally disable dragging to prevent panning
    });

    if (!L.gridLayer.googleMutant) {
        console.error('GoogleMutant plugin not loaded');
        return;
    }

    L.gridLayer.googleMutant({
        type: 'hybrid',
        maxZoom: 18,
        key: googleMapsKey
    }).addTo(map.value);

    // Draw the polygon on the map if coordinates are available
    if (coordinates.value && coordinates.value.length) {
        const polygon = L.polygon(coordinates.value, { color: 'red' }).addTo(map.value);

        // Fit the map view to the polygon bounds
        map.value.fitBounds(polygon.getBounds());
    } else {
        console.error('No coordinates available to draw on the map.');
    }
};

onMounted(() => {
    const farmId = getFarmIdFromUrl();
    if (farmId) {
        fetchFarmZoneData(farmId);
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