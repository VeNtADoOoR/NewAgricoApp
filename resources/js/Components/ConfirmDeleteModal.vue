<template>
    <transition name="fade">
      <div v-if="isVisible" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="bg-white p-5 border border-gray-300 rounded shadow-lg relative">
          <h2 class="text-lg font-semibold mb-4">Are you sure you want to delete "{{ farmName }}"?</h2>
          <div class="flex justify-end gap-4">
            <button @click="confirmDelete" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-400 transition duration-200">
              Delete
            </button>
            <button @click="cancelDelete" class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-400 transition duration-200">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </transition>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    isVisible: Boolean,
    farmName: String
  });
  
  const emit = defineEmits(['confirm', 'cancel']);
  
  const confirmDelete = () => {
    emit('confirm');
  };
  
  const cancelDelete = () => {
    emit('cancel');
  };
  </script>
  
  <style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  