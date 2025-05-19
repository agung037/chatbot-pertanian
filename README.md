# AgroBot - Tomato Disease Detection and Farm Assistant

A comprehensive web application for tomato farmers to detect plant diseases and get cultivation advice.

## Features

- **Disease Detection**: Upload an image to identify tomato plant diseases
- **AI Chat Assistant**: Get expert advice on tomato cultivation
- **Forum**: Connect with other farmers to share knowledge and experiences
- **Dashboard**: View analytics and statistics

## Project Architecture

### Backend (Flask)

The backend is built using Flask with a modular architecture:

- **Application Factory Pattern**: Centralized app configuration and initialization
- **Blueprints**: Organized routes by feature
- **Service Layer**: Separation of business logic from routes
- **Dependency Injection**: Services are loosely coupled for better testability
- **Configuration Management**: Environment-specific configurations

#### Directory Structure

```
backend/
├── app.py                 # Application factory and entry point
├── wsgi.py                # WSGI entry point for production
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── models/                # ML model implementations
│   ├── __init__.py
│   └── plant_disease_model.py
├── routes/                # API routes organized by feature
│   ├── __init__.py
│   ├── chat.py
│   ├── disease.py
│   └── general.py
├── services/              # Business logic and external services
│   ├── __init__.py
│   ├── disease_service.py
│   ├── llm_service.py
│   └── service_registry.py
└── utils/                 # Utility functions and helpers
    ├── __init__.py
    ├── api.py
    ├── disease_data.py
    ├── image_processing.py
    ├── llm.py
    ├── model_prediction.py
    └── swagger.py
```

### Frontend

The frontend uses HTML, CSS (TailwindCSS), and JavaScript:

- **Webpack**: For bundling and optimization
- **TailwindCSS**: For styling
- **Modular JavaScript**: Organized by feature

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- API keys (see `.env.example`)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chatbot-pertanian.git
   cd chatbot-pertanian
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   FLASK_ENV=development
   ```

4. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend:
   ```
   cd backend
   python app.py
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:9000`

## API Endpoints

The API is organized around RESTful principles:

- **Chat API**: `/api/chat`
  - `POST /`: Send a message to the chatbot
  - `GET /health`: Check chat service availability

- **Disease Detection API**: `/api/disease`
  - `POST /detect`: Detect disease from base64 image
  - `POST /detect-file`: Detect disease from uploaded file
  - `GET /health`: Check disease detection service availability

- **General API**: 
  - `GET /`: Serve the main page
  - `GET /api/health`: Overall API health check
  - `GET /api/test`: Simple test endpoint

### Swagger Documentation

The API includes Swagger documentation for easy exploration and testing:

- Access Swagger UI at: `http://localhost:5012/docs`
- Alternative access via: `http://localhost:5012/swagger`

The Swagger UI provides:
- Interactive documentation for all API endpoints
- Request/response models and schemas
- Testing interface to make API calls directly from the browser
- Authentication requirements and error handling information

### OpenAPI Specification

The OpenAPI specification for the API can be accessed at:
- `http://localhost:5012/swagger.json`

This JSON file contains the complete API specification that can be imported into tools like Postman, Insomnia, or other API development environments.

## Deployment

The application can be deployed using Gunicorn for the backend:

```
cd backend
gunicorn wsgi:application
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
