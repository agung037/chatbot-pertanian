<template>
  <div class="w-64 bg-white dark:bg-agrobot-dark-card border-r border-gray-200 dark:border-gray-700 p-4 h-screen overflow-y-auto flex-shrink-0">
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 dark:text-white mb-4">AgroBot</h2>
      <nav>
        <ul>
          <li class="mb-2">
            <router-link to="/" class="flex items-center px-4 py-2 rounded-lg transition-colors" :class="{ 'text-blue-600 bg-blue-50 dark:bg-blue-900 dark:text-blue-200': $route.path === '/', 'text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-700': $route.path !== '/' }">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Dashboard
            </router-link>
          </li>
          <li class="mb-2">
            <router-link to="/detection" class="flex items-center px-4 py-2 rounded-lg transition-colors" :class="{ 'text-blue-600 bg-blue-50 dark:bg-blue-900 dark:text-blue-200': $route.path === '/detection', 'text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-700': $route.path !== '/detection' }">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
              Detection Disease
            </router-link>
          </li>
          <li class="mb-2">
            <router-link to="/forum" class="flex items-center px-4 py-2 rounded-lg transition-colors" :class="{ 'text-blue-600 bg-blue-50 dark:bg-blue-900 dark:text-blue-200': $route.path === '/forum', 'text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-700': $route.path !== '/forum' }">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
              </svg>
              Forum
            </router-link>
          </li>
          <li class="mb-2">
            <router-link to="/chat" class="flex items-center px-4 py-2 rounded-lg transition-colors" :class="{ 'text-blue-600 bg-blue-50 dark:bg-blue-900 dark:text-blue-200': $route.path === '/chat', 'text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-gray-700': $route.path !== '/chat' }">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              AI Assistant Chat
            </router-link>
          </li>
        </ul>
      </nav>
    </div>
    
    <div class="mt-auto pt-6">
      <div class="bg-blue-50 dark:bg-gray-700 p-3 rounded-lg">
        <div class="text-sm text-gray-700 dark:text-gray-300">
          <p class="font-medium mb-1">API Status</p>
          <div class="flex items-center space-x-2 text-xs">
            <span class="w-3 h-3 rounded-full" :class="apiStatus ? 'bg-green-500' : 'bg-red-500'"></span>
            <span>{{ apiStatus ? 'Connected' : 'Disconnected' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      apiStatus: false,
      statusInterval: null
    };
  },
  mounted() {
    this.checkApiStatus();
    // Check API status every 30 seconds
    this.statusInterval = setInterval(this.checkApiStatus, 30000);
  },
  beforeUnmount() {
    // Clear interval when component is destroyed
    if (this.statusInterval) {
      clearInterval(this.statusInterval);
    }
  },
  methods: {
    async checkApiStatus() {
      try {
        const response = await fetch('http://localhost:5012/api/health');
        const data = await response.json();
        // The backend returns "ok" or other values for status
        this.apiStatus = data.status === 'ok' || data.status === 'success' || data.status === 'healthy';
      } catch (error) {
        this.apiStatus = false;
        console.error('Failed to check API status:', error);
      }
    }
  }
};
</script> 