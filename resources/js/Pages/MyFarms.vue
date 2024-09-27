<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import AuthNavBar from '@/Components/AuthNavBar.vue';
import SideBar from '@/Components/SideBar.vue';
import ConfirmDeleteModal from '@/Components/ConfirmDeleteModal.vue';
import UpdateFarmModal from '@/Components/UpdateFarmModal.vue';

const farms = ref([]);
const showDeleteModal = ref(false);
const showUpdateModal = ref(false);
const farmToDelete = ref(null);
const farmToUpdate = ref(null);

// Fetch user's farms when the component is mounted
onMounted(async () => {
  await fetchFarms();
});

const fetchFarms = async () => {
  try {
    const response = await axios.get('/api/farm-zone');
    farms.value = response.data;
  } catch (error) {
    console.error('Error loading the farms:', error);
  }
};

const showDeleteModalHandler = (farm) => {
  farmToDelete.value = farm;
  showDeleteModal.value = true;
};

const deleteFarmZone = async () => {
  if (farmToDelete.value) {
    try {
      await axios.delete(`/api/farm-zone/${farmToDelete.value.id}`);
      await fetchFarms(); // Refresh the farms list
      showDeleteModal.value = false;
    } catch (error) {
      console.error('Error deleting farm zone:', error);
      alert('Error deleting the farm zone.');
    }
  }
};

const cancelDelete = () => {
  showDeleteModal.value = false;
};

const showUpdateFarmModal = (farm) => {
  farmToUpdate.value = farm;
  showUpdateModal.value = true;
};

const handleUpdate = async () => {
  await fetchFarms(); // Refresh the farms list
};

const cancelUpdate = () => {
  showUpdateModal.value = false;
};

</script>


<template>
  <div class="container mx-auto bg-green-100" style="width: 100%;">
    <AuthNavBar />
    <div class="flex">
      <SideBar />
      <div class="flex-1">
        <!-- Check if farms list is empty -->
        <div v-if="farms.length === 0" class="p-6 text-center text-gray-700 font-bold">
          <h1>You have no registered farms!</h1>
        </div>
        <div v-else>
          <table class="min-w-full divide-y divide-gray-200 border border-gray-300 my-3">
            <thead class="bg-green-700">
              <tr>
                <th class="px-6 py-3 text-left text-sm font-medium text-white uppercase tracking-wider">Farm Name</th>
                <th class="px-6 py-3 text-left text-sm font-medium text-white uppercase tracking-wider">Area(ha)</th>
                <th class="px-6 py-3 text-left text-sm font-medium text-white uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="farm in farms" :key="farm.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ farm.farm_name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ farm.farm_area }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <a :href="`/farm-view/${farm.id}`">
                    <button
                      class="bg-green-700 text-white px-4 py-2 rounded hover:bg-green-500 transition duration-200">
                      View
                    </button>
                  </a>
                  <button @click="showUpdateFarmModal(farm)"
                    class="bg-yellow-500 text-white px-4 py-2 rounded mx-4 hover:bg-yellow-400 transition duration-200">Change
                    the name</button>
                  <button @click="showDeleteModalHandler(farm)"
                    class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-400 transition duration-200">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Confirmation modal -->
    <ConfirmDeleteModal :isVisible="showDeleteModal" :farmName="farmToDelete?.farm_name" @confirm="deleteFarmZone"
      @cancel="cancelDelete" />

    <!-- Update Farm Modal -->
    <UpdateFarmModal :isVisible="showUpdateModal" :farmName="farmToUpdate?.farm_name" :farmId="farmToUpdate?.id"
      @update="handleUpdate" @cancel="cancelUpdate" />
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
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.05em;
}
</style>
