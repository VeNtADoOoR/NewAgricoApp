<template>
    <div class="max-w-4xl mx-auto mt-10 p-6 bg-white shadow-md rounded-md">
        <h2 class="text-2xl font-bold mb-6 text-center text-green-700">Image Processing Interface</h2>
        
        <div class="mb-4">
            <input 
                type="file" 
                @change="onFileChange" 
                class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none" 
                accept="image/*"
            />
        </div>
        
        <div class="flex justify-between mb-6">
            <button 
                @click="uploadImage" 
                class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
                Upload Image
            </button>
            <button 
                @click="processImage('radiometric')" 
                class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
                Apply Radiometric Correction
            </button>
            <button 
                @click="processImage('atmospheric')" 
                class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
                Apply Atmospheric Correction
            </button>
        </div>

        <div class="flex justify-between mb-6">
            <button 
                @click="calculateIndex('NDVI')" 
                class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
                Calculate NDVI
            </button>
            <button 
                @click="calculateIndex('EVI')" 
                class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition duration-200"
            >
                Calculate EVI
            </button>
        </div>
        
        <div v-if="result" class="mt-6">
            <h3 class="text-xl font-semibold text-center text-green-700 mb-4">Result</h3>
            <img :src="result.processedImagePath" alt="Processed Image" class="max-w-full mx-auto mb-4 border rounded" />
            <p v-if="result.indexValue" class="text-center text-gray-700 font-medium">Vegetation Index: {{ result.indexValue }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const selectedFile = ref(null);
const result = ref(null);

const onFileChange = (event) => {
    selectedFile.value = event.target.files[0];
};

const uploadImage = async () => {
    if (!selectedFile.value) return alert('Please select an image file first.');

    const formData = new FormData();
    formData.append('image', selectedFile.value);

    try {
        const response = await axios.post('/upload-image', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        alert('Image uploaded successfully.');
        result.value = { imagePath: response.data.imagePath };
    } catch (error) {
        console.error(error);
        alert('Failed to upload image.');
    }
};

const processImage = async (correctionType) => {
    if (!result.value || !result.value.imagePath) return alert('Please upload an image first.');

    try {
        const response = await axios.post('/process-image', {
            imagePath: result.value.imagePath,
            correctionType,
        });
        result.value.processedImagePath = response.data.processedImagePath;
        alert(`${correctionType} correction applied successfully.`);
    } catch (error) {
        console.error(error);
        alert(`Failed to apply ${correctionType} correction.`);
    }
};

const calculateIndex = async (indexType) => {
    if (!result.value || !result.value.imagePath) return alert('Please upload an image first.');

    try {
        const response = await axios.post('/calculate-vegetation-index', {
            imagePath: result.value.imagePath,
            indexType,
        });
        result.value.indexValue = response.data.value;
        alert(`${indexType} calculated successfully.`);
    } catch (error) {
        console.error(error);
        alert(`Failed to calculate ${indexType}.`);
    }
};
</script>

<style scoped>
/* Additional custom styles can go here */
</style>
