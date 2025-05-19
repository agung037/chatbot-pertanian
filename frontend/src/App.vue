<template>
  <div class="min-h-screen">
    <div class="flex h-screen overflow-hidden">
      <!-- Sidebar -->
      <Sidebar />
      
      <!-- Main content -->
      <main class="flex-1 overflow-y-auto bg-agrobot-bg">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: 'App',
  components: {
    Sidebar
  }
}
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --agrobot-bg: #f5f7fa;
  --agrobot-dark-bg: #1a202c;
  --agrobot-dark-card: #2d3748;
  --agrobot-dark-text: #e2e8f0;
}

.bg-agrobot-bg {
  background-color: var(--agrobot-bg);
}

.dark .bg-agrobot-dark-bg {
  background-color: var(--agrobot-dark-bg);
}

.dark .bg-agrobot-dark-card {
  background-color: var(--agrobot-dark-card);
}

.dark .text-agrobot-dark-text {
  color: var(--agrobot-dark-text);
}

body {
  font-family: 'Poppins', sans-serif;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #3b82f6;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 