<template>
  <div class="p-8">
    <div class="container mx-auto max-w-4xl">
      <div class="flex justify-between items-center mb-5">
        <h1 class="text-2xl font-semibold text-gray-800 dark:text-white">AgroBot, your agro assistant</h1>
        <button 
          @click="clearHistory"
          class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors"
        >
          Clear History
        </button>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-5">
        <div @click="toggleBotInfo" class="flex justify-between items-center cursor-pointer">
          <h2 class="text-lg font-medium text-gray-800 dark:text-white">Tentang AgroBot</h2>
          <span :class="{ 'transform rotate-180': botInfoOpen }" class="transition-transform text-gray-800 dark:text-white">▼</span>
        </div>
        <div :class="{ 'hidden': !botInfoOpen }" class="mt-3">
          <p class="text-gray-700 dark:text-gray-300 mb-2">
            AgroBot adalah asisten pertanian berbasis AI yang dirancang untuk membantu petani, profesional pertanian, dan penggemar pertanian dengan pertanyaan terkait pertanian mereka.
          </p>
          <ul class="list-disc list-inside text-gray-600 dark:text-gray-400">
            <li>Perawatan tanaman dan teknik budidaya</li>
            <li>Pengelolaan hama dan penyakit</li>
            <li>Pengelolaan tanah dan pemupukan</li>
            <li>Praktik pertanian terbaik</li>
            <li>Saran umum tentang pertanian</li>
          </ul>
          <div class="text-sm text-gray-500 dark:text-gray-500 mt-3">
            Didukung oleh: Llama3-8b-8192 (Groq)
          </div>
        </div>
      </div>

      <div ref="chatMessages" class="bg-white dark:bg-agrobot-dark-card border border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-5 h-[450px] overflow-y-auto">
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-300 dark:text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p class="text-gray-500 dark:text-gray-400">Ayo mulai percakapan dengan AgroBot!</p>
        </div>
        
        <div v-else v-for="(message, index) in messages" :key="index" class="mb-4">
          <div :class="message.sender === 'user' ? 'bg-blue-50 dark:bg-blue-900 text-gray-800 dark:text-gray-100 ml-8' : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-100 mr-8'" class="p-3 rounded-lg">
            <div class="flex items-start">
              <div v-if="message.sender === 'bot'" class="w-8 h-8 rounded-full bg-green-500 flex-shrink-0 flex items-center justify-center text-white font-bold mr-2">
                A
              </div>
              <div v-else class="w-8 h-8 rounded-full bg-blue-500 flex-shrink-0 flex items-center justify-center text-white font-bold mr-2">
                U
              </div>
              <div>
                <p class="whitespace-pre-line">{{ message.text }}</p>
                <span class="text-xs text-gray-500 dark:text-gray-400 mt-1 block">{{ formatTime(message.timestamp) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="isLoading" class="flex items-center space-x-2 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg mr-8 mb-4">
          <div class="w-8 h-8 rounded-full bg-green-500 flex-shrink-0 flex items-center justify-center text-white font-bold">
            A
          </div>
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-500 dark:bg-gray-400 rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-gray-500 dark:bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-gray-500 dark:bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="flex gap-2">
        <input 
          v-model="userInput"
          type="text" 
          placeholder="Ketik pertanyaan Anda di sini..." 
          class="flex-grow px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 rounded text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="isLoading"
          required
        >
        <button 
          type="submit" 
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:hover:bg-blue-500"
          :disabled="isLoading"
        >
          Kirim
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue';

export default {
  name: 'Chat',
  setup() {
    const userInput = ref('');
    const messages = ref([]);
    const isLoading = ref(false);
    const botInfoOpen = ref(false);
    const chatMessages = ref(null);

    // Load messages from localStorage on component mount
    onMounted(() => {
      const savedMessages = localStorage.getItem('chatMessages');
      if (savedMessages) {
        messages.value = JSON.parse(savedMessages);
      }
      scrollToBottom();
    });

    // Save messages to localStorage whenever they change
    watch(messages, (newMessages) => {
      localStorage.setItem('chatMessages', JSON.stringify(newMessages));
      nextTick(() => {
        scrollToBottom();
      });
    }, { deep: true });

    function scrollToBottom() {
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      }
    }

    function toggleBotInfo() {
      botInfoOpen.value = !botInfoOpen.value;
    }

    function formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    async function sendMessage() {
      if (!userInput.value.trim()) return;
      
      // Add user message
      messages.value.push({
        sender: 'user',
        text: userInput.value,
        timestamp: Date.now()
      });
      
      const userMessage = userInput.value;
      userInput.value = '';
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: userMessage }),
        });
        
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Add bot response
        messages.value.push({
          sender: 'bot',
          text: data.response,
          timestamp: Date.now()
        });
      } catch (error) {
        console.error('Error sending message:', error);
        
        // Add error message
        messages.value.push({
          sender: 'bot',
          text: 'Maaf, terjadi kesalahan saat menghubungi server. Silakan coba lagi nanti.',
          timestamp: Date.now()
        });
      } finally {
        isLoading.value = false;
      }
    }

    function clearHistory() {
      if (confirm('Apakah Anda yakin ingin menghapus semua riwayat percakapan?')) {
        messages.value = [];
        localStorage.removeItem('chatMessages');
      }
    }

    return {
      userInput,
      messages,
      isLoading,
      botInfoOpen,
      chatMessages,
      sendMessage,
      clearHistory,
      toggleBotInfo,
      formatTime
    };
  }
};
</script> 