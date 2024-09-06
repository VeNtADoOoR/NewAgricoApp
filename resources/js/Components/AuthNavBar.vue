<template>
    <div>
        <nav class="bg-green-700">
            <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
                <div class="relative flex h-16 items-center justify-between">
                    <!-- Logo -->
                    <div class="flex items-center hover:cursor-pointer">
                        <img src="/images/plant.png" alt="Logo" class="h-8 w-auto" />
                        <h2 class="ml-2 text-white text-xl font-semibold">AgricoApp</h2>
                    </div>

                    <!-- Mobile menu button -->
                    <div class="absolute inset-y-0 right-0 flex items-center sm:hidden">
                        <button @click="isOpen = !isOpen"
                            class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-green-900 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                            <span class="sr-only">Open main menu</span>
                            <svg v-if="!isOpen" class="block h-6 w-6" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 6h16M4 12h16m-7 6h7"></path>
                            </svg>
                            <svg v-else class="block h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>

                    <!-- Navbar Content for larger screens -->
                    <div class="hidden sm:flex flex-1 items-center justify-end space-x-6">
                        <!-- Notifications Icon -->
                        <button class="text-white hover:text-green-200 focus:outline-none">
                            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 10-4 0v1.341C8.67 6.165 7 8.388 7 11v3.159c0 .538-.214 1.055-.595 1.436L5 17h5m4 0v1a2 2 0 11-4 0v-1m4 0H9">
                                </path>
                            </svg>
                        </button>

                        <!-- User Profile -->
                        <div class="relative">
                            <div class="flex items-center space-x-2 cursor-pointer"
                                @click="userDropdownOpen = !userDropdownOpen">
                                <!-- User photo with fallback -->
                                <img :src="userPhoto" alt="User Photo"
                                    class="h-8 w-8 rounded-full border-2 border-white" />
                                <span class="text-white font-medium">{{ fullName }}</span>
                                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </div>
                            <!-- Dropdown Menu -->
                            <div v-if="userDropdownOpen" 
                                class="absolute right-0 mt-2 w-48 bg-green-100 rounded-md shadow-lg py-1 z-50">
                                <ResponsiveNavLink to="/profile"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile
                                </ResponsiveNavLink>
                                <ResponsiveNavLink to="/settings"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings
                                </ResponsiveNavLink>
                                <!-- Updated Logout Form -->
                                <form method="POST" @submit.prevent="logout">
                                    <ResponsiveNavLink as="button"
                                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Log Out
                                    </ResponsiveNavLink>
                                </form>
                            </div>
                        </div>
                    </div>

                    <!-- Mobile menu items -->
                    <div v-if="isOpen" class="sm:hidden absolute top-16 left-0 w-full bg-green-700">
                        <div class="flex flex-col items-center space-y-4 py-4">
                            <!-- Notifications Icon -->
                            <button class="text-gray-400 hover:text-white focus:outline-none">
                                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 10-4 0v1.341C8.67 6.165 7 8.388 7 11v3.159c0 .538-.214 1.055-.595 1.436L5 17h5m4 0v1a2 2 0 11-4 0v-1m4 0H9">
                                    </path>
                                </svg>
                            </button>

                            <!-- User Profile -->
                            <div class="flex items-center space-x-2 cursor-pointer"
                                @click="userDropdownOpen = !userDropdownOpen">
                                <!-- User photo with fallback for mobile -->
                                <img :src="userPhoto" alt="User Photo"
                                    class="h-8 w-8 rounded-full border-2 border-white" />
                                <span class="text-white font-medium">{{ fullName }}</span>
                                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 9l-7 7-7-7"></path>
                                </svg>
                            </div>

                            <!-- Dropdown Menu for mobile -->
                            <div v-if="userDropdownOpen" class="w-48 bg-green-200 rounded-md shadow-lg py-1">
                                <a href="/profile"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
                                <a href="/settings"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
                                <!-- Updated Logout Link for mobile -->
                                <form method="POST" @submit.prevent="logout">
                                    <button type="submit"
                                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                                        Log Out
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { usePage } from '@inertiajs/vue3';
import ResponsiveNavLink from './ResponsiveNavLink.vue';
import axios from 'axios';

const isOpen = ref(false);
const userDropdownOpen = ref(false);

const { props } = usePage();
const user = props.auth.user;
const userPhoto = ref(user?.profile_photo_path || '/images/default-user-photo.jpg');
const fullName = ref(`${user?.first_name} ${user?.last_name}`);

const logout = async () => {
    try {
        await axios.post('/logout'); // Perform the POST request to Laravel's logout route
        window.location.href = '/'; // Redirect to login page after successful logout
    } catch (error) {
        console.error('Logout failed', error);
    }
};
</script>


<style scoped>
/* Additional custom styles can go here if needed */
</style>
