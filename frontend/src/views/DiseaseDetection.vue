<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold mb-6 text-red-800 dark:text-red-300">Tomato Disease Detection</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6 border-l-4 border-red-500">
        <h2 class="text-xl font-semibold mb-4 text-red-700 dark:text-red-400">Upload Tomato Leaf Image</h2>
        <div 
          ref="dropArea" 
          @dragover.prevent="handleDragOver" 
          @dragleave.prevent="handleDragLeave" 
          @drop.prevent="handleDrop"
          :class="{'border-red-500': isDragging, 'border-gray-300 dark:border-gray-700': !isDragging}"
          class="border-2 border-dashed rounded-lg p-6 text-center transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-4 text-red-400 dark:text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p class="text-gray-500 dark:text-gray-400 mb-4">Drag and drop a tomato leaf image or click to upload</p>
          <input type="file" ref="imageUpload" @change="handleFileSelect" class="hidden" accept="image/*">
          <button 
            @click="$refs.imageUpload.click()" 
            class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors font-medium">
            Choose Image
          </button>
        </div>
        <div v-if="previewUrl" class="mt-4">
          <h3 class="text-lg font-medium mb-2 text-red-700 dark:text-red-400">Image Preview</h3>
          <div class="relative">
            <img :src="previewUrl" alt="Preview" class="w-full h-auto rounded-lg max-h-64 object-contain">
            <button 
              @click="removeImage" 
              class="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full hover:bg-red-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <button 
            @click="detectDisease" 
            :disabled="isDetecting"
            class="mt-4 bg-red-700 text-white px-4 py-2 rounded hover:bg-red-800 transition-colors w-full disabled:opacity-50 disabled:cursor-not-allowed font-medium">
            {{ isDetecting ? 'Detecting...' : 'Detect Disease' }}
          </button>
        </div>
      </div>

      <div class="bg-white dark:bg-agrobot-dark-card rounded-lg shadow-md p-6 border-l-4 border-red-500">
        <h2 class="text-xl font-semibold mb-4 text-red-700 dark:text-red-400">Detection Results</h2>
        <div v-if="!detectionResult && !isDetecting" class="space-y-4">
          <div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-4 text-center">
            <p class="text-red-800 dark:text-red-300">Upload a tomato leaf image to detect diseases</p>
          </div>
        </div>
        <div v-if="isDetecting" class="mt-4 flex justify-center items-center">
          <div class="spinner mr-3 border-red-700"></div>
          <p class="text-red-800 dark:text-red-300">Analyzing image...</p>
        </div>
        <div v-if="detectionResult" class="space-y-4">
          <div v-if="detectionResult.status === 'loading'" class="bg-red-100 dark:bg-red-900/50 p-4 rounded-lg">
            <h3 class="font-semibold text-red-900 dark:text-red-100">Model is loading</h3>
            <p class="text-red-800 dark:text-red-200">Please try again in a few seconds</p>
          </div>
          
          <div v-else-if="detectionResult.error" class="bg-red-100 dark:bg-red-900/50 p-4 rounded-lg">
            <h3 class="font-semibold text-red-900 dark:text-red-100">Error</h3>
            <p class="text-red-800 dark:text-red-200">{{ detectionResult.error }}</p>
          </div>
          
          <div v-else class="bg-red-100 dark:bg-red-900/50 p-4 rounded-lg">
            <h3 class="font-semibold text-red-900 dark:text-red-100 mb-2">Detection Results</h3>
            <div class="flex justify-between items-center">
              <span class="font-medium text-red-800 dark:text-red-200">{{ formatDiseaseName(detectionResult.prediction) }}</span>
              <span class="text-red-800 dark:text-red-200">{{ (detectionResult.confidence * 100).toFixed(2) }}% confidence</span>
            </div>
          </div>
          
          <div v-if="detectionResult.llmInfo" class="mt-4 bg-red-50 dark:bg-red-900/30 p-6 rounded-lg">
            <h3 class="font-semibold text-red-900 dark:text-red-200 text-xl mb-4">Informasi Detail Penyakit</h3>
            <div class="text-red-800 dark:text-red-300 space-y-2" v-html="formatLLMResponse(detectionResult.llmInfo)"></div>
          </div>
          
          <div v-if="detectionResult.prediction && !isFetchingGroqSuggestion">
            <button 
              @click="getGroqSuggestion"
              class="mt-4 bg-red-700 text-white px-4 py-2 rounded hover:bg-red-800 transition-colors w-full font-medium"
              :disabled="isLoadingGroqSuggestion">
              {{ isLoadingGroqSuggestion ? 'Mendapatkan saran...' : 'Dapatkan Saran Penanganan dari Groq' }}
            </button>
          </div>
          
          <div v-if="groqSuggestion" class="mt-4 bg-red-50 dark:bg-red-900/20 p-6 rounded-lg">
            <h3 class="font-semibold text-red-900 dark:text-red-200 text-xl mb-4">Saran Penanganan</h3>
            <div class="text-red-800 dark:text-red-300 space-y-2" v-html="formatGroqSuggestion(groqSuggestion)"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiseaseDetection',
  data() {
    return {
      selectedFile: null,
      previewUrl: null,
      isDetecting: false,
      isDragging: false,
      detectionResult: null,
      groqSuggestion: null,
      isLoadingGroqSuggestion: false
    };
  },
  methods: {
    handleDragOver() {
      this.isDragging = true;
    },
    handleDragLeave() {
      this.isDragging = false;
    },
    handleDrop(e) {
      this.isDragging = false;
      if (e.dataTransfer.files.length) {
        this.processFile(e.dataTransfer.files[0]);
      }
    },
    handleFileSelect() {
      const file = this.$refs.imageUpload.files[0];
      if (file) {
        this.processFile(file);
      }
    },
    processFile(file) {
      this.selectedFile = file;
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewUrl = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    removeImage() {
      this.selectedFile = null;
      this.previewUrl = null;
      this.detectionResult = null;
      this.groqSuggestion = null;
      this.$refs.imageUpload.value = '';
    },
    async detectDisease() {
      if (!this.selectedFile) {
        alert('Please select an image first');
        return;
      }
      
      this.isDetecting = true;
      this.detectionResult = null;
      this.groqSuggestion = null;
      
      try {
        // Create FormData
        const formData = new FormData();
        formData.append('image', this.selectedFile);
        
        // Send to backend
        const response = await fetch('/api/disease/detect-file', {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        this.detectionResult = result;
      } catch (error) {
        console.error('Error detecting disease:', error);
        this.detectionResult = {
          error: error.message || 'An error occurred while detecting disease'
        };
      } finally {
        this.isDetecting = false;
      }
    },
    async getGroqSuggestion() {
      if (!this.detectionResult || !this.detectionResult.prediction) {
        return;
      }
      
      this.isLoadingGroqSuggestion = true;
      
      try {
        const response = await fetch('/api/disease/suggestion', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            disease: this.detectionResult.prediction,
            language: 'id'
          })
        });
        
        if (!response.ok) {
          throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        this.groqSuggestion = result.suggestion;
      } catch (error) {
        console.error('Error getting Groq suggestion:', error);
        this.groqSuggestion = 'Maaf, terjadi kesalahan saat meminta saran dari Groq';
      } finally {
        this.isLoadingGroqSuggestion = false;
      }
    },
    formatDiseaseName(name) {
      if (!name) return '';
      
      // Replace underscores with spaces
      let formatted = name.replace(/_/g, ' ');
      
      // Replace "Tomato___" prefix
      formatted = formatted.replace('Tomato ', '');
      
      // Capitalize words
      return formatted
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
    },
    formatLLMResponse(text) {
      if (!text) return '';
      
      // Remove extra whitespace and normalize line breaks
      text = text.replace(/\s+/g, ' ').trim();
      
      // Extract disease name if present (wrapped in **)
      let diseaseName = '';
      const diseaseMatch = text.match(/\*\*(.*?)\*\*/);
      if (diseaseMatch) {
        diseaseName = diseaseMatch[1];
        text = text.replace(/\*\*.*?\*\*\s*/, ''); // Remove disease name from text
      }
      
      // Split sections by headers (wrapped in **)
      const sections = text.split(/\*\*(.*?)\*\*/);
      
      let formattedText = '';
      
      // Add disease name if found
      if (diseaseName) {
        formattedText += `
          <div class="mb-6 bg-red-50 dark:bg-red-900/30 p-4 rounded-lg">
            <h3 class="text-xl font-bold text-red-800 dark:text-red-200">${diseaseName}</h3>
          </div>
        `;
      }
      
      // Process each section
      for (let i = 1; i < sections.length; i += 2) {
        const title = sections[i];
        let content = sections[i + 1] || '';
        
        // Process bullet points
        content = content.replace(/\*/g, '•');  // Replace * with bullet points
        content = content.replace(/\+/g, '•');  // Replace + with bullet points
        
        // Split content into paragraphs and bullet points
        const lines = content.split(/[•]/).filter(line => line.trim());
        
        formattedText += `
          <div class="mb-6">
            <h4 class="text-lg font-semibold text-red-900 dark:text-red-200 mb-3">${title}</h4>
            <div class="text-red-800 dark:text-red-300 space-y-2">
        `;
        
        if (lines.length > 1) {
          formattedText += '<ul class="list-disc space-y-2 ml-5">';
          lines.forEach(line => {
            if (line.trim()) {
              formattedText += `<li class="text-red-800 dark:text-red-300">${line.trim()}</li>`;
            }
          });
          formattedText += '</ul>';
        } else {
          formattedText += `<p>${content.trim()}</p>`;
        }
        
        formattedText += '</div></div>';
      }
      
      return formattedText;
    },
    formatGroqSuggestion(text) {
      if (!text) return '';
      
      // Simple formatting for Groq suggestions
      // Replace line breaks with proper HTML
      const formattedText = text
        .split('\n\n')
        .map(paragraph => `<p class="mb-3">${paragraph}</p>`)
        .join('');
        
      return formattedText;
    }
  }
};
</script>

<style scoped>
.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: currentColor;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 