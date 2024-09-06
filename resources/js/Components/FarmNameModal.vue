<template>
    <div v-if="visible" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="bg-green-100 p-4 rounded shadow-lg">
            <h2 class="text-lg font-semibold">Enter Farm Name</h2>
            <input v-model="farmName" type="text" placeholder="Farm Name"
                class="mt-2 p-2 border border-gray-300 rounded" />
            <div class="mt-4 flex justify-end space-x-2">
                <button @click="cancel" class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-400">Cancel</button>
                <button @click="submit" class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500">Submit</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
    visible: Boolean
});

const emits = defineEmits(['submit', 'cancel']);

const farmName = ref('');

const submit = () => {
    emits('submit', farmName.value);
};

const cancel = () => {
    emits('cancel');
};
</script>