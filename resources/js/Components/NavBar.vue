<template>
    <div>
        <nav class="bg-green-700">
            <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
                <div class="relative flex h-16 items-center justify-between">
                    <!-- Logo -->
                    <router-link to="/welcome" class="absolute left-0 flex items-center hover:cursor-pointer">
                        <img src="/images/plant.png" alt="Logo" class="h-8 w-auto" />
                        <h2 class="text-white">AgricoApp</h2>
                    </router-link>

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

                    <!-- Navbar Content -->
                    <div class="flex flex-1 items-center justify-end space-x-4">
                        <div v-if="!isOpen" class="hidden sm:flex space-x-4">
                            <a :href="route('login')">
                                <button
                                    class="bg-green-900 text-white px-4 py-2 rounded-md hover:bg-green-800">Login</button>
                            </a>
                            <a :href="route('register')">
                                <button class="bg-green-900 text-white px-4 py-2 rounded-md hover:bg-green-800">Sign
                                    Up</button>
                            </a>
                        </div>
                    </div>

                    <!-- Mobile menu items -->
                    <div v-if="isOpen" class="sm:hidden">
                        <div class="space-y-1 px-2 pb-3 pt-2">
                            <a :href="route('login')">
                                <button
                                    class="w-full text-left bg-green-900 text-white px-4 py-2 rounded-md hover:bg-green-800">Login</button>
                            </a>
                            <a :href="route('register')">
                                <button
                                    class="w-full text-left bg-green-900 text-white px-4 py-2 rounded-md hover:bg-green-800">Sign
                                    Up</button>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    </div>
</template>
<script setup>
    import { ref, onMounted } from 'vue';
    const isOpen = ref(false);
</script>
<style scoped>
nav {
    position: relative;
}
</style>