<template>
    <div class="flex h-screen bg-white">
        <!-- Sidebar -->
        <div :class="isOpen ? 'block' : 'hidden lg:block'"
            class="bg-green-700 text-white w-64 space-y-6 px-2 py-7 absolute lg:relative lg:translate-x-0 transform transition-transform duration-200">
            <!-- Navigation -->
            <nav class="mt-10">
                <a href="/dashboard"
                    :class="isActive('/dashboard') ? activeClass : inactiveClass"
                    @click.prevent="setActive('/dashboard')">
                    Dashboard
                </a>
                <a href="/interactive-map"
                    :class="isActive('/interactive-map') ? activeClass : inactiveClass"
                    @click.prevent="setActive('/interactive-map')">
                    Interactive Map
                </a>
                <a href="/my-farms"
                    :class="isActive('/my-farms') ? activeClass : inactiveClass"
                    @click.prevent="setActive('/my-farms')">
                    My farms
                </a>
                <a href="/reports"
                    :class="isActive('/reports') ? activeClass : inactiveClass"
                    @click.prevent="setActive('/reports')">
                    Reports
                </a>
                <a href="/notifications"
                    :class="isActive('/notifications') ? activeClass : inactiveClass"
                    @click.prevent="setActive('/notifications')">
                    Notifications
                </a>
            </nav>
        </div>

        <!-- Main content -->
        <div class="flex-1 p-2 bg-green-100">
            <!-- Toggle Button for Sidebar on Small Screens -->
            <button @click="toggleSidebar" class="lg:hidden text-gray-800 hover:text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                    class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isOpen = ref(false);
const activePath = ref(window.location.pathname); // Initialize with the current path

const toggleSidebar = () => {
    isOpen.value = !isOpen.value;
};

// Classes for active and inactive links
const activeClass = 'block py-2.5 px-4 rounded bg-green-500 text-white';
const inactiveClass = 'block py-2.5 px-4 rounded transition duration-200 hover:bg-green-500 hover:text-white';

// Function to check if the path is active
const isActive = (path) => {
    return activePath.value === path;
};

// Function to set the active path and navigate
const setActive = (path) => {
    activePath.value = path;
    window.location.href = path; // Navigate to the path
};

// Ensure activePath is set correctly on page load
onMounted(() => {
    activePath.value = window.location.pathname;
});
</script>

<style scoped>
/* Optional styles for transitions and behavior */
</style>
