<template>
  <div class="flex items-center justify-center h-full p-8">
    <div class="text-center">
      <div class="text-9xl font-bold text-gray-300 dark:text-gray-700">404</div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white mt-4">Page Not Found</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">The page you are looking for doesn't exist or has been moved.</p>
      <div class="mt-6">
        <router-link to="/" class="inline-flex items-center px-5 py-2 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          Back to Dashboard
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
};
</script> 