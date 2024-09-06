<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AuthNavBar from '@/Components/AuthNavBar.vue';
import SideBar from '@/Components/SideBar.vue';

const farms = ref([]);

// Fetch user's farms when the component is mounted
onMounted(async () => {
  try {
    const response = await axios.get('/api/farm-zone');
    farms.value = response.data;
  } catch (error) {
    console.error('Error fetching farms:', error);
  }
});

// Define methods for the actions

</script>

<template>
  <div class="container mx-auto bg-green-100" style="width: 100%;">
    <AuthNavBar />
    <div class="flex">
      <SideBar />
      <div class="flex-1">
        <table class="min-w-full divide-y divide-gray-200 border border-gray-300 my-3">
          <thead class="bg-green-700">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-medium text-white uppercase tracking-wider">Farm Name</th>
              <th class="px-6 py-3 text-left text-sm font-medium text-white uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="farm in farms" :key="farm.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ farm.farm_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-400 transition duration-200">View</button>
                <button class="bg-yellow-500 text-white px-4 py-2 rounded mx-2 hover:bg-yellow-400 transition duration-200">Edit</button>
                <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-400 transition duration-200">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
table {
  border-radius: 10px;
}

th {
  text-align: center;
}

td {
  height: 60px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.05em;
}
</style>
