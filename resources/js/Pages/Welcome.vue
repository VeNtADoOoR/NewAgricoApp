<script setup>
import NavBar from '@/Components/NavBar.vue';

const sections = [
    {
        title: "Analyse satellite images",
        description: "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maiores impedit perferendis suscipit eaque, iste dolor cupiditate blanditiis ratione.",
        image: "/images/agrico-satellite.jpeg" // Absolute path from the public directory
    },
    {
        title: "Interactive map",
        description: "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maiores impedit perferendis suscipit eaque, iste dolor cupiditate blanditiis ratione.",
        image: "/images/map.jpg" // Absolute path from the public directory
    },
    {
        title: "Easy decision taking",
        description: "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maiores impedit perferendis suscipit eaque, iste dolor cupiditate blanditiis ratione.",
        image: "/images/solution.jpg" // Absolute path from the public directory
    },
];
</script>

<template>
    <div class="container w-full mx-auto">
        
        <NavBar/>

        <div class="relative py-24 sm:py-32 min-h-[600px] flex items-center">
            <img src="/images/agrico-back.jpg" alt="Background Image"
                class="absolute inset-0 -z-10 h-full w-full object-cover object-center" />
            <div class="absolute inset-0 bg-black opacity-50"></div>
            <div class="relative mx-auto max-w-7xl px-6 lg:px-8 text-center">
                <div class="relative mx-auto max-w-2xl lg:mx-0 py-8">
                    <h1 class="text-4xl font-bold tracking-tight text-white sm:text-8xl mb-4">Welcome to AgricoApp</h1>
                    <p class="text-base leading-8 sm:text-2xl text-white">We provide the best AI solutions for
                        agriculture!</p>
                </div>
            </div>
        </div>

        <div v-for="(section, index) in sections" :key="index"
            class="overflow-hidden py-24 sm:py-32 bg-green-700 bg-opacity-30 rounded-xl my-2 sm:my-12 lg:my-5">
            <div class="mx-auto max-w-7xl px-6 lg:px-8">
                <div
                    class="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 sm:gap-y-20 lg:mx-0 lg:max-w-none lg:grid-cols-2">

                    <!-- Image Section (order based on index) -->
                    <div v-if="index % 2 === 0" class="flex items-center justify-center lg:order-first">
                        <div class="relative w-[48rem] h-[30rem] rounded-xl overflow-hidden">
                            <img :src="section.image" alt="Product screenshot"
                                class="absolute inset-0 w-full h-full rounded-xl shadow-xl ring-1 ring-gray-400/10 object-cover" />
                        </div>
                    </div>

                    <!-- Text Section -->
                    <div
                        :class="{ 'lg:pr-8 lg:pt-4 flex items-center justify-center': index % 2 === 0, 'lg:pl-8 lg:pt-4 flex items-center justify-center': index % 2 !== 0 }">
                        <div class="lg:max-w-lg">
                            <p class="mt-2 text-3xl font-bold tracking-tight text-green-900 sm:text-4xl">{{
                                section.title }}</p>
                            <p class="mt-6 text-lg leading-8 text-green-700">{{ section.description }}</p>
                        </div>
                    </div>

                    <!-- Image Section (order based on index) -->
                    <div v-if="index % 2 !== 0" class="flex items-center justify-center">
                        <div class="relative w-[48rem] h-[30rem] rounded-xl overflow-hidden">
                            <img :src="section.image" alt="Product screenshot"
                                class="absolute inset-0 w-full h-full rounded-xl shadow-xl ring-1 ring-gray-400/10 object-cover" />
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <footer class="bg-green-700 text-white py-6">
            <div class="mx-auto max-w-7xl px-6 lg:px-8 text-center">
                <p class="text-sm">&copy; 2024 AgricoApp. All rights reserved.</p>
            </div>
        </footer>

    </div>
</template>


<style scoped>
</style>