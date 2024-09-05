<script setup>
import AuthNavBar from '@/Components/AuthNavBar.vue';
import SideBar from '@/Components/SideBar.vue';
</script>

<template>

  <div class="container mx-auto" style="width: 100%;">
    <AuthNavBar/>
    <div class="flex">
      <SideBar/>
      <div class="flex-1">
        <h1>Here you can see a list of your farms</h1>
      </div>
    </div>
  </div>
</template>

<style scoped></style>