<template>
    <div class="container mx-auto bg-green-100" style="width: 100%;">
        <AuthNavBar />
        <div class="flex flex-nowrap justify-between items-start py-4">
            <!-- First Map -->
            <div class="w-1/2 mr-4">
                <div id="map1" class="leaflet-container" style="height: 600px; border: 1rem solid green;"></div>

                <div class="flex flex-row">
                    <!-- the first calendar -->
                    <div
                        class="flex flex-row sm:flex-row items-start sm:items-center mt-5 space-y-3 sm:space-y-0 sm:space-x-3 mr-3">
                        <input type="date" id="date" v-model="selectedDate"
                            class="p-3 w-full sm:w-auto border border-gray-300 rounded-md shadow-md focus:outline-none
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out hover:shadow-lg" />
                    </div>
                    <button
                        class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3">
                        NDVI</button>
                    <button
                        class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3">
                        EVI</button>
                    <button
                        class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3">
                        NDWI</button>
                </div>

            </div>

            <!-- Second Map -->
            <div class="w-1/2">
                <div id="map2" class="leaflet-container" style="height: 600px; border: 1rem solid green;"></div>
                <div class="flex flex-row">
                    <!-- the first calendar -->
                    <div
                        class="flex flex-row sm:flex-row items-start sm:items-center mt-5 space-y-3 sm:space-y-0 sm:space-x-3 mr-3">
                        <input type="date" id="date" v-model="selectedDate"
                            class="p-3 w-full sm:w-auto border border-gray-300 rounded-md shadow-md focus:outline-none
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out hover:shadow-lg" />
                    </div>
                    <button
                        class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3">
                        NDVI</button>
                    <button
                        class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3">
                        EVI</button>
                    <button
                        class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3">
                        NDWI</button>
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
import AuthNavBar from '@/Components/AuthNavBar.vue';

const googleMapsKey = ''; // Your Google Maps API key
const coordinates = ref([]);
const farmId = ref(null);
const selectedDate = ref();

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
        initializeMaps();
    } catch (error) {
        console.error('Error fetching farm zone data:', error);
    }
};

const convertCoordinates = (coords) => {
    return coords[0].map(coord => [coord[1], coord[0]]);
};

const initializeMaps = () => {
    // Initialize the first map
    const map1 = L.map('map1', {
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
    }).addTo(map1);

    if (coordinates.value && coordinates.value.length) {
        const polygon1 = L.polygon(coordinates.value, { color: 'red', fillOpacity: 0, weight: 3 }).addTo(map1);
        map1.fitBounds(polygon1.getBounds());
    }

    // Initialize the second map
    const map2 = L.map('map2', {
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
    }).addTo(map2);

    if (coordinates.value && coordinates.value.length) {
        const polygon2 = L.polygon(coordinates.value, { color: 'red', fillOpacity: 0, weight: 3 }).addTo(map2);
        map2.fitBounds(polygon2.getBounds());
    }
};

onMounted(() => {
    farmId.value = getFarmIdFromUrl();
    fetchFarmZoneData(farmId.value);
});
</script>

<style scoped>
.leaflet-container {
    height: 100%;
    width: 100%;
    z-index: 10;
}
</style>