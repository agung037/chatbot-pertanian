# AgroBot - Agricultural Assistant

## Demo
![AgroBot Demo](demo.gif)


AgroBot is an AI-powered agricultural assistant designed to help farmers, agricultural professionals, and farming enthusiasts with agricultural-related questions and plant disease detection.

## Features

### AI Chatbot Assistant
- Real-time chat interface with an AI assistant specialized in agricultural topics
- Persistent chat history using localStorage
- Responsive design for desktop and mobile devices

### Tomato Disease Detection
- Image-based disease detection using machine learning
- Upload images via drag-and-drop or file selection
- Detailed disease classification with confidence percentages
- Disease information and treatment recommendations in English
- **NEW:** Comprehensive disease information in Indonesian language using LLM

### Forum Discussions
- Community forum for agricultural discussions
- Ask questions and share knowledge with other farmers

### Knowledge Base
- Dashboard with agricultural information and best practices
- Searchable resources for common farming issues

## Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- TailwindCSS for styling
- Responsive design across devices

### Backend
- Python with Flask web framework
- RESTful API with Flask-RESTX and Swagger documentation
- CORS support for cross-origin requests

### AI and Machine Learning
- Groq API integration with Llama3-8b-8192 model for chatbot
- HuggingFace API for disease detection (MobileNet model)
- LLM-generated content in multiple languages

## Installation and Setup

### Prerequisites
- Python 3.8+ installed
- API keys from Groq and HuggingFace
- Git for cloning the repository

### Step 1: Clone the Repository
```bash
git clone https://github.com/agung037/chatbot-pertanian.git
cd chatbot-pertanian
```

### Step 2: Set Up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Configure API Keys
Create a `.env` file in the backend directory with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Access the Web Interface
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## API Endpoints

### Chat Endpoints
- `POST /chat`: Send messages to the AI assistant
  - Request: `{ "message": "your question here" }`
  - Response: `{ "response": "AI assistant's answer" }`

### Disease Detection Endpoints
- `POST /detect-disease`: Detect diseases in plant images
  - Request: `{ "image": "base64_encoded_image", "requestLlmInfo": true }`
  - Response: Contains disease prediction, confidence score, and LLM-generated information

### Other Endpoints
- `GET /test`: Test if the API is running
- Swagger UI available at `/docs` for interactive API documentation

## Usage Instructions

### Chatbot Assistant
1. Navigate to the AI Assistant page
2. Type your agricultural question in the chat input
3. Receive expert advice in Indonesian language

### Disease Detection
1. Go to the Disease Detection page
2. Upload a tomato leaf image
3. Click "Detect Disease"
4. View the classification results with confidence scores
5. Read detailed information about the disease, including:
   - English description and treatment options
   - Comprehensive Indonesian information about symptoms, causes, and treatments

## Troubleshooting

- If you see a "Model is loading" message, wait a few seconds and try again
- Ensure images are clear and well-lit for accurate detection
- Make sure your API keys are correctly configured
- Check that you're using a supported image format (JPG, PNG)

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
