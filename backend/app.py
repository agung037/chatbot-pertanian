import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
import logging
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Import utility modules
from utils.image_processing import process_image_data, detect_image_format
from utils.disease_data import enrich_disease_data
from utils.llm import create_chat_messages, create_disease_info_prompt
from utils.api import call_huggingface_api, parse_huggingface_response
from utils.swagger import api, chat_ns, disease_ns, general_ns
from utils.swagger import (chat_request, chat_response, error_response, 
                         disease_response, loading_response, test_response,
                         image_parser, json_parser)
from models.plant_disease_model import PlantDiseaseModel
from flask_restx import Resource

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

# Initialize Swagger documentation
api.init_app(app)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Get API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Validate API keys
if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not set. Please configure it in .env file")
    
if not HUGGINGFACE_API_KEY:
    logger.warning("HUGGINGFACE_API_KEY not set. Please configure it in .env file")

# Initialize Groq client
try:
    groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    groq_client = None

# Initialize the plant disease model
try:
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'tomato_disease.h5')
    plant_disease_model = PlantDiseaseModel(model_path)
    logger.info("Plant disease model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize plant disease model: {e}")
    plant_disease_model = None

# Routes
@app.route('/')
def index():
    """Serve the main chat page."""
    return render_template('index.html')

# Swagger API routes
@chat_ns.route('')
class ChatAPI(Resource):
    @chat_ns.doc('chat_with_bot')
    @chat_ns.expect(chat_request)
    @chat_ns.response(200, 'Success', chat_response)
    @chat_ns.response(400, 'Validation Error', error_response)
    @chat_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Send a message to the chatbot and get a response"""
        # Validate configuration
        if not groq_client:
            return {"error": "Groq client not initialized. Check your API Key."}, 500
        if not GROQ_API_KEY:
            return {"error": "GROQ_API_KEY not configured on server."}, 500

        try:
            # Get user message
            data = request.json
            user_message = data.get('message')
            if not user_message:
                return {"error": "Message cannot be empty."}, 400

            logger.info(f"Message received from user: {user_message}")

            # Create prompt for Groq
            messages = create_chat_messages(user_message)

            # Send request to Groq API
            chat_completion = groq_client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192",
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            bot_response = chat_completion.choices[0].message.content
            return {"response": bot_response}, 200

        except Exception as e:
            logger.error(f"Error in chat endpoint: {e}", exc_info=True)
            return {"error": str(e)}, 500

@disease_ns.route('/detect')
class DiseaseDetectionAPI(Resource):
    @disease_ns.doc('detect_disease')
    @disease_ns.expect(json_parser)
    @disease_ns.response(200, 'Success', disease_response)
    @disease_ns.response(400, 'Validation Error', error_response)
    @disease_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Detect plant disease from base64 encoded image"""
        if not plant_disease_model:
            return {"error": "Plant disease model not initialized"}, 500
        if not groq_client:
            return {"error": "Groq client not initialized. Check your API Key."}, 500

        try:
            # Get image data from request
            data = request.json
            if not data or 'image' not in data:
                return {"error": "No image data provided"}, 400

            # Process image data
            image_bytes = process_image_data(data['image'])
            if not image_bytes:
                return {"error": "Invalid image data"}, 400

            # Make prediction
            result = plant_disease_model.predict(image_bytes)
            
            # Get LLM information about the disease
            if result and 'prediction' in result:
                try:
                    disease_name = result['prediction']
                    messages = create_disease_info_prompt(disease_name)
                    
                    # Send request to Groq API
                    logger.info(f"Requesting LLM info for disease: {disease_name}")
                    chat_completion = groq_client.chat.completions.create(
                        messages=messages,
                        model="llama3-8b-8192",
                        temperature=0.7,
                        max_tokens=1024,
                        top_p=1,
                        stop=None,
                        stream=False,
                    )
                    
                    # Extract response and add to result
                    llm_info = chat_completion.choices[0].message.content
                    logger.info(f"Generated LLM info for {disease_name}: {llm_info[:50]}...")
                    result['llmInfo'] = llm_info
                except Exception as llm_err:
                    logger.error(f"Error generating LLM information: {llm_err}")
                    result['llmInfoError'] = "Failed to generate disease information"
            
            return result, 200

        except Exception as e:
            logger.error(f"Error in disease detection: {e}", exc_info=True)
            return {"error": str(e)}, 500

@disease_ns.route('/detect-file')
class DiseaseDetectionFileAPI(Resource):
    @disease_ns.doc('detect_disease_file')
    @disease_ns.expect(image_parser)
    @disease_ns.response(200, 'Success', disease_response)
    @disease_ns.response(400, 'Validation Error', error_response)
    @disease_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Detect plant disease from uploaded image file"""
        if not plant_disease_model:
            return {"error": "Plant disease model not initialized"}, 500

        try:
            # Get image file from request
            if 'image' not in request.files:
                return {"error": "No image file provided"}, 400

            image_file = request.files['image']
            if not image_file:
                return {"error": "Empty image file"}, 400

            # Read image file
            image_bytes = image_file.read()
            if not image_bytes:
                return {"error": "Could not read image file"}, 400

            # Make prediction
            result = plant_disease_model.predict(image_bytes)
            
            # Enrich the result with additional disease information
            enriched_result = enrich_disease_data(result)
            
            return enriched_result, 200

        except Exception as e:
            logger.error(f"Error in disease detection from file: {e}", exc_info=True)
            return {"error": str(e)}, 500

@general_ns.route('/test')
class TestAPI(Resource):
    @general_ns.doc('test_api')
    @general_ns.response(200, 'Success', test_response)
    def get(self):
        """Test the API health"""
        return {"status": "healthy", "message": "API is running"}, 200

# Legacy routes for backward compatibility
@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Legacy route for chat functionality"""
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok", "message": "Preflight OK"}), 200
    
    # Forward to the API route
    api_response = ChatAPI().post()
    if isinstance(api_response, tuple):
        return jsonify(api_response[0]), api_response[1]
    return jsonify(api_response)

@app.route('/detect-disease', methods=['POST', 'OPTIONS'])
def detect_disease():
    """Legacy route for disease detection"""
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok", "message": "Preflight OK"}), 200
    
    # Forward to the API route based on the type of request
    if request.files and 'image' in request.files:
        api_response = DiseaseDetectionFileAPI().post()
    else:
        api_response = DiseaseDetectionAPI().post()
    
    # If the request includes a request for LLM information, add it to the response
    if request.is_json and request.json.get('requestLlmInfo') and isinstance(api_response, dict):
        try:
            # Check if groq client is available
            if not groq_client:
                logger.warning("Skipping LLM info generation: Groq client not initialized")
            else:
                # Get the top disease prediction
                prediction = api_response.get('prediction', [])
                if isinstance(prediction, list) and len(prediction) > 0:
                    top_disease = prediction[0]
                    disease_name = top_disease.get('label')
                    
                    if disease_name:
                        # Create prompt for disease information
                        messages = create_disease_info_prompt(disease_name)
                        
                        # Send request to Groq API
                        logger.info(f"Requesting LLM info for disease: {disease_name}")
                        chat_completion = groq_client.chat.completions.create(
                            messages=messages,
                            model="llama3-8b-8192",
                            temperature=0.7,
                            max_tokens=1024,
                            top_p=1,
                            stop=None,
                            stream=False,
                        )
                        
                        # Extract response and add to API response
                        llm_info = chat_completion.choices[0].message.content
                        logger.info(f"Generated LLM info for {disease_name}: {llm_info[:50]}...")
                        
                        # Add to response
                        api_response['llmInfo'] = llm_info
        except Exception as e:
            logger.error(f"Error generating LLM information: {e}", exc_info=True)
            api_response['llmInfoError'] = "Failed to generate LLM information"
        
    if isinstance(api_response, tuple):
        return jsonify(api_response[0]), api_response[1]
    return jsonify(api_response)

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Legacy route for test endpoint"""
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 