<template>
    <div class="container mx-auto bg-green-100" style="width: 100%;">
        <AuthNavBar />
        <div class="flex flex-col">
            <div class="flex flex-nowrap justify-between items-start py-4">
                <!-- First Map -->
                <div class="w-1/2 mr-4">
                    <div id="map1" class="leaflet-container" style="height: 600px; border: 1rem solid green;"></div>
                </div>
                <!-- Second Map -->
                <div class="w-1/2">
                    <div id="map2" class="leaflet-container" style="height: 600px; border: 1rem solid green;"></div>
                </div>
            </div>
            <div class="flex flex-row justify-center mb-2">
                <div class="flex flex-row items-start mt-5 space-y-3 sm:space-y-0 sm:space-x-3 mr-3">
                    <input type="date" id="date1" v-model="selectedDate1"
                        class="p-3 w-full sm:w-auto border border-gray-300 rounded-md shadow-md focus:outline-none
                        focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out hover:shadow-lg" />
                </div>
                <button
                    class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3 w-20"
                    @click="fetchNDVI" :disabled="NdviLoading">
                    <span v-if="NdviLoading"
                        class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-t-transparent rounded-full"></span>
                    <span v-if="!NdviLoading">NDVI</span>
                </button>
                <button
                    class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3 w-20"
                    @click="fetchEVI" :disabled="EviLoading">
                    <span v-if="EviLoading"
                        class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-t-transparent rounded-full"></span>
                    <span v-if="!EviLoading">EVI</span>
                </button>
                <button
                    class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200 mt-5 mx-3 w-20"
                    @click="fetchNDII" :disabled="NdiiLoading">
                    <span v-if="NdiiLoading"
                        class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-t-transparent rounded-full"></span>
                    <span v-if="!NdiiLoading">NDII</span>
                </button>
                <div class="flex flex-row items-start mt-5 space-y-3 sm:space-y-0 sm:space-x-3 mr-3">
                    <input type="date" id="date2" v-model="selectedDate2"
                        class="p-3 w-full sm:w-auto border border-gray-300 rounded-md shadow-md focus:outline-none
                        focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-300 ease-in-out hover:shadow-lg" />
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
const selectedDate1 = ref();
const selectedDate2 = ref();
const map1 = ref(null);
const map2 = ref(null);
const ndviLayer1 = ref(null);
const ndviLayer2 = ref(null);
const eviLayer1 = ref(null);
const eviLayer2 = ref(null);
const ndiiLayer1 = ref(null);
const ndiiLayer2 = ref(null);
const NdviLoading = ref(false); // Track NDVI loading state
const EviLoading = ref(false); // Track EVI loading state
const NdiiLoading = ref(false); // Track NDII loading state

const getFarmIdFromUrl = () => {
    const url = new URL(window.location.href);
    return url.pathname.split('/').pop(); // Get the last part of the URL
};

const removeLayerIfExists = (map, layer) => {
    if (layer.value) {
        map.value.removeLayer(layer.value);
    }
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
    map1.value = L.map('map1', {
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
    }).addTo(map1.value);

    if (coordinates.value && coordinates.value.length) {
        const polygon1 = L.polygon(coordinates.value, { color: 'red', fillOpacity: 0, weight: 3 }).addTo(map1.value);
        map1.value.fitBounds(polygon1.getBounds());
    }

    // Initialize the second map
    map2.value = L.map('map2', {
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
    }).addTo(map2.value);

    if (coordinates.value && coordinates.value.length) {
        const polygon2 = L.polygon(coordinates.value, { color: 'red', fillOpacity: 0, weight: 3 }).addTo(map2.value);
        map2.value.fitBounds(polygon2.getBounds());
    }
};

const fetchNDVI = async () => {
    if (selectedDate1.value && selectedDate2.value) {
        NdviLoading.value = true;
        try {
            const response = await axios.get(`/api/farm-zone/${farmId.value}/ndvi-comparison`, {
                params: {
                    date1: selectedDate1.value,
                    date2: selectedDate2.value,
                }
            });
            const { tileUrlDate1, tileUrlDate2 } = response.data;

            // Call the function for each layer
            removeLayerIfExists(map1, ndviLayer1);
            removeLayerIfExists(map1, eviLayer1);
            removeLayerIfExists(map1, ndiiLayer1);

            ndviLayer1.value = L.tileLayer(tileUrlDate1, { opacity: 0.8, attribution: 'NDVI Layer for Date 1' }).addTo(map1.value);

            removeLayerIfExists(map2, ndviLayer2);
            removeLayerIfExists(map2, eviLayer2);
            removeLayerIfExists(map2, ndiiLayer2);
            ndviLayer2.value = L.tileLayer(tileUrlDate2, { opacity: 0.8, attribution: 'NDVI Layer for Date 2' }).addTo(map2.value);

        } catch (error) {
            console.error('Error fetching NDVI data:', error);
        }
        finally {
            NdviLoading.value = false; // End loading
        }
    } else {
        alert('Please select both dates.');
    }

};

const fetchEVI = async () => {
    if (selectedDate1.value && selectedDate2.value) {
        EviLoading.value = true;
        try {
            const response = await axios.get(`/api/farm-zone/${farmId.value}/evi-comparison`, {
                params: {
                    date1: selectedDate1.value,
                    date2: selectedDate2.value,
                }
            });
            const { tileUrlDate1, tileUrlDate2 } = response.data;

            removeLayerIfExists(map1, ndviLayer1);
            removeLayerIfExists(map1, eviLayer1);
            removeLayerIfExists(map1, ndiiLayer1);
            eviLayer1.value = L.tileLayer(tileUrlDate1, { opacity: 0.8, attribution: 'EVI Layer for Date 1' }).addTo(map1.value);

            removeLayerIfExists(map2, ndviLayer2);
            removeLayerIfExists(map2, eviLayer2);
            removeLayerIfExists(map2, ndiiLayer2);
            eviLayer2.value = L.tileLayer(tileUrlDate2, { opacity: 0.8, attribution: 'EVI Layer for Date 2' }).addTo(map2.value);

        } catch (error) {
            console.error('Error fetching EVI data:', error);
        }
        finally {
            EviLoading.value = false; // End loading
        }
    } else {
        alert('Please select both dates.');
    }
};

const fetchNDII = async () => {
    if (selectedDate1.value && selectedDate2.value) {
        NdiiLoading.value = true;
        try {
            const response = await axios.get(`/api/farm-zone/${farmId.value}/ndii-comparison`, {
                params: {
                    date1: selectedDate1.value,
                    date2: selectedDate2.value,
                }
            });
            const { tileUrlDate1, tileUrlDate2 } = response.data;

            removeLayerIfExists(map1, ndviLayer1);
            removeLayerIfExists(map1, eviLayer1);
            removeLayerIfExists(map1, ndiiLayer1);
            ndiiLayer1.value = L.tileLayer(tileUrlDate1, { opacity: 0.8, attribution: 'NDII Layer for Date 1' }).addTo(map1.value);

            removeLayerIfExists(map2, ndviLayer2);
            removeLayerIfExists(map2, eviLayer2);
            removeLayerIfExists(map2, ndiiLayer2);
            ndiiLayer2.value = L.tileLayer(tileUrlDate2, { opacity: 0.8, attribution: 'NDII Layer for Date 2' }).addTo(map2.value);

        } catch (error) {
            console.error('Error fetching NDII data:', error);
        }
        finally {
            NdiiLoading.value = false; // End loading
        }
    } else {
        alert('Please select both dates.');
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
