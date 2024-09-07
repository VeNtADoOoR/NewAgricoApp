<!-- src/Components/UpdateFarmModal.vue -->
<template>
    <div v-if="isVisible" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
        <div class="bg-white p-6 rounded shadow-lg">
            <h3 class="text-lg font-semibold mb-4">Update Farm Name</h3>
            <input v-model="newFarmName" type="text" class="border border-gray-300 rounded p-2 w-full mb-4" />
            <div class="flex justify-end">
                <button @click="updateFarm"
                    class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-400 transition duration-200">Update</button>
                <button @click="cancelUpdate"
                    class="bg-gray-500 text-white px-4 py-2 rounded ml-4 hover:bg-gray-400 transition duration-200">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref, defineEmits, defineProps } from 'vue';

const props = defineProps({
    isVisible: Boolean,
    farmName: String,
    farmId: Number
});

const emit = defineEmits(['update', 'cancel']);

const newFarmName = ref(props.farmName);

const updateFarm = async () => {
    try {
        await axios.put(`/api/farm-zone/${props.farmId}`, { farm_name: newFarmName.value });
        emit('update');
        farms.value = farms.value.filter(farm => farm.id !== farmToDelete.value.id);
    } catch (error) {
        console.error('Error updating farm name:', error);
        alert('Error updating farm name.');
    }
};

const cancelUpdate = () => {
    emit('cancel');
};
</script>