<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white">Agricultural Forum</h1>
      <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
        Create New Topic
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800 dark:text-white">Crop Cultivation</h2>
          <span class="text-sm text-gray-500 dark:text-gray-400">12 Topics</span>
        </div>
        <ul class="space-y-3">
          <li v-for="(topic, index) in cropTopics" :key="index" class="flex items-center justify-between">
            <a href="#" class="text-blue-600 dark:text-blue-400 hover:underline">{{ topic.title }}</a>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ topic.replies }} replies</span>
          </li>
        </ul>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800 dark:text-white">Pest Management</h2>
          <span class="text-sm text-gray-500 dark:text-gray-400">9 Topics</span>
        </div>
        <ul class="space-y-3">
          <li v-for="(topic, index) in pestTopics" :key="index" class="flex items-center justify-between">
            <a href="#" class="text-blue-600 dark:text-blue-400 hover:underline">{{ topic.title }}</a>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ topic.replies }} replies</span>
          </li>
        </ul>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-800 dark:text-white">Agricultural Technology</h2>
          <span class="text-sm text-gray-500 dark:text-gray-400">7 Topics</span>
        </div>
        <ul class="space-y-3">
          <li v-for="(topic, index) in techTopics" :key="index" class="flex items-center justify-between">
            <a href="#" class="text-blue-600 dark:text-blue-400 hover:underline">{{ topic.title }}</a>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ topic.replies }} replies</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="mt-8 bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Recent Discussions</h2>
      <div class="space-y-4">
        <div v-for="(discussion, index) in recentDiscussions" :key="index" class="border-b dark:border-gray-700 pb-4">
          <div class="flex justify-between items-center mb-2">
            <a href="#" class="text-lg font-medium text-blue-600 dark:text-blue-400 hover:underline">{{ discussion.title }}</a>
            <span class="text-sm text-gray-500 dark:text-gray-400">Posted by @{{ discussion.author }}</span>
          </div>
          <p class="text-gray-600 dark:text-gray-300 text-sm">{{ discussion.summary }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Forum',
  data() {
    return {
      cropTopics: [
        { title: 'Best Practices for Rice Farming', replies: 5 },
        { title: 'Organic Vegetable Gardening', replies: 8 },
        { title: 'Sustainable Farming Techniques', replies: 12 }
      ],
      pestTopics: [
        { title: 'Natural Pest Control Methods', replies: 7 },
        { title: 'Identifying Common Crop Pests', replies: 15 },
        { title: 'Integrated Pest Management', replies: 10 }
      ],
      techTopics: [
        { title: 'IoT in Agriculture', replies: 6 },
        { title: 'Drone Technology in Farming', replies: 9 },
        { title: 'AI in Agriculture', replies: 11 }
      ],
      recentDiscussions: [
        {
          title: 'Improving Soil Fertility Naturally',
          author: 'AgriExpert',
          summary: 'Discussing organic methods to enhance soil nutrients without chemical fertilizers...'
        },
        {
          title: 'Climate Change Impact on Agriculture',
          author: 'ClimateAgri',
          summary: 'Exploring adaptive strategies for farmers facing changing climate conditions...'
        },
        {
          title: 'Smart Irrigation Techniques',
          author: 'WaterWise',
          summary: 'Sharing innovative water conservation methods in agricultural irrigation...'
        }
      ]
    };
  }
};
</script> 