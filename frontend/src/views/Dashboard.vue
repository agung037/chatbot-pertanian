<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 dark:text-white">Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Agricultural Insights Cards -->
      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-700 dark:text-gray-200">Crop Health</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-gray-500 dark:text-gray-400">Overall crop health: Good</p>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div class="bg-green-600 h-2.5 rounded-full" style="width: 85%"></div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-700 dark:text-gray-200">Soil Moisture</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 7.777 16.656 10.657c.563 2.88-.002 5.346-1.346 7.657z" />
          </svg>
        </div>
        <p class="text-gray-500 dark:text-gray-400">Current moisture level: 65%</p>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div class="bg-blue-600 h-2.5 rounded-full" style="width: 65%"></div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-700 dark:text-gray-200">Pest Risk</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <p class="text-gray-500 dark:text-gray-400">Current risk level: Moderate</p>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div class="bg-yellow-600 h-2.5 rounded-full" style="width: 45%"></div>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-gray-700 dark:text-gray-200">Yield Prediction</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        <p class="text-gray-500 dark:text-gray-400">Estimated yield: 85 tons/hectare</p>
        <div class="mt-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div class="bg-purple-600 h-2.5 rounded-full" style="width: 75%"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Recent Activities</h2>
        <ul class="space-y-3">
          <li class="flex items-center">
            <span class="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
            <span class="text-gray-600 dark:text-gray-300">Soil fertilization completed</span>
          </li>
          <li class="flex items-center">
            <span class="w-3 h-3 bg-blue-500 rounded-full mr-3"></span>
            <span class="text-gray-600 dark:text-gray-300">Irrigation system checked</span>
          </li>
          <li class="flex items-center">
            <span class="w-3 h-3 bg-yellow-500 rounded-full mr-3"></span>
            <span class="text-gray-600 dark:text-gray-300">Pest monitoring initiated</span>
          </li>
        </ul>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Upcoming Tasks</h2>
        <ul class="space-y-3">
          <li class="flex items-center justify-between">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-gray-600 dark:text-gray-300">Crop Rotation Planning</span>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Next Week</span>
          </li>
          <li class="flex items-center justify-between">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 01-4.176-3.97L9.22 7.666a1 1 0 00-.853-.706l-1.285-.193a1 1 0 00-1.145.817l-.767 5.378a1 1 0 00.965 1.138h.908a1 1 0 00.99-.858l.567-4.055a6.067 6.067 0 012.328 3.123l.728 2.768a1 1 0 00.553.662l2.527 1.23a1 1 0 001.412-.522l1.014-2.477a1 1 0 00-.1-.894z" />
              </svg>
              <span class="text-gray-600 dark:text-gray-300">Fertilizer Application</span>
            </div>
            <span class="text-sm text-gray-500 dark:text-gray-400">In 2 Weeks</span>
          </li>
        </ul>
      </div>
    </div>
    
    <!-- Monthly Harvest Heatmap -->
    <div class="mt-8 bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Harvest Distribution by Month</h2>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr>
              <th class="py-2 text-left text-gray-600 dark:text-gray-300">Crop</th>
              <th v-for="month in months" :key="month" class="py-2 text-center text-gray-600 dark:text-gray-300">{{ month }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(crop, index) in harvestData" :key="index" class="border-t border-gray-200 dark:border-gray-700">
              <td class="py-3 text-gray-600 dark:text-gray-300">{{ crop.name }}</td>
              <td v-for="(value, monthIndex) in crop.values" :key="monthIndex" class="py-2 px-1">
                <div class="w-full h-8 rounded" 
                     :style="{ backgroundColor: getHeatmapColor(value), opacity: 0.2 + (value / 100) * 0.8 }"
                     :title="`${crop.name}: ${value} tons`">
                  <div class="flex justify-center items-center h-full text-xs font-medium" 
                       :class="value > 60 ? 'text-gray-800 dark:text-white' : 'text-gray-700 dark:text-gray-300'">
                    {{ value }}
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-4 flex justify-end">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-500 dark:text-gray-400">Low</span>
          <div class="flex space-x-1">
            <div class="w-4 h-4 rounded" style="background-color: #fee0d2;"></div>
            <div class="w-4 h-4 rounded" style="background-color: #fc9272;"></div>
            <div class="w-4 h-4 rounded" style="background-color: #de2d26;"></div>
          </div>
          <span class="text-sm text-gray-500 dark:text-gray-400">High</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      harvestData: [
        {
          name: 'Rice',
          values: [10, 15, 35, 65, 80, 95, 75, 60, 45, 30, 20, 15]
        },
        {
          name: 'Corn',
          values: [5, 10, 25, 45, 75, 90, 85, 70, 45, 25, 15, 10]
        },
        {
          name: 'Soybeans',
          values: [30, 45, 65, 85, 95, 80, 60, 40, 35, 25, 20, 25]
        },
        {
          name: 'Cassava',
          values: [70, 80, 85, 75, 55, 40, 35, 30, 45, 60, 75, 65]
        },
        {
          name: 'Chili',
          values: [40, 50, 65, 80, 85, 75, 60, 45, 40, 35, 30, 35]
        }
      ]
    }
  },
  methods: {
    getHeatmapColor(value) {
      // Tomato/red gradient for the heatmap
      if (value < 30) return '#fee0d2';
      if (value < 70) return '#fc9272';
      return '#de2d26';
    }
  }
}
</script> 