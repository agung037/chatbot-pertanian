import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
import logging

# Import utility modules
from utils.image_processing import process_image_data, detect_image_format
from utils.disease_data import enrich_disease_data
from utils.llm import create_chat_messages, create_disease_info_prompt
from utils.api import call_huggingface_api, parse_huggingface_response
from utils.swagger import api, chat_ns, disease_ns, general_ns
from utils.swagger import (chat_request, chat_response, error_response, 
                         disease_response, loading_response, test_response,
                         image_parser, json_parser)
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
CORS(app, resources={
    r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]},
    r"/docs": {"origins": "*"},
    r"/swagger.json": {"origins": "*"},
    r"/chat": {"origins": "*", "methods": ["POST", "OPTIONS"], "allow_headers": ["Content-Type"]},
    r"/detect-disease": {"origins": "*", "methods": ["POST", "OPTIONS"], "allow_headers": ["Content-Type"]}
})

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
            logger.info(f"Response from Groq: {bot_response[:100]}...")

            return {"response": bot_response}

        except Exception as e:
            logger.error(f"Error contacting Groq API or processing request: {e}", exc_info=True)
            
            # Include Groq error details if available
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None and hasattr(e.response, 'json'):
                try:
                    error_detail = e.response.json()
                    if isinstance(error_detail, dict) and 'error' in error_detail:
                        error_message = f"{str(e)} - Detail: {error_detail['error']}"
                except:
                    pass
                    
            return {"error": f"Sorry, an internal error occurred: {error_message}"}, 500

@disease_ns.route('/detect')
class DiseaseDetectionAPI(Resource):
    @disease_ns.doc('detect_disease')
    @disease_ns.expect(json_parser)
    @disease_ns.response(200, 'Success', disease_response)
    @disease_ns.response(202, 'Model Loading', loading_response)
    @disease_ns.response(400, 'Validation Error', error_response)
    @disease_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Detect diseases in tomato plant images (base64 encoded)"""
        if not HUGGINGFACE_API_KEY:
            logger.error("HuggingFace API Key not configured")
            return {"error": "HuggingFace API Key not configured on server."}, 500
        
        try:
            # Process image from request
            try:
                image_bytes = process_image_data(request.json if request.is_json else {})
            except ValueError as img_err:
                logger.error(f"Error processing image: {img_err}")
                return {"error": str(img_err)}, 400
            
            # Call HuggingFace API
            huggingface_url = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
            
            # Set headers with content type
            content_type = detect_image_format(image_bytes)
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                "Content-Type": content_type
            }
            
            # Make API call
            try:
                response = call_huggingface_api(huggingface_url, headers, image_bytes)
                result = parse_huggingface_response(response)
                
                # Check if model is loading
                if isinstance(result, dict) and result.get("status") == "loading":
                    return result, 202
                    
            except (ConnectionError, ValueError) as api_err:
                return {"error": str(api_err)}, 500
            
            # Filter for tomato-specific results if possible
            if isinstance(result, list):
                tomato_results = [item for item in result if item.get("label") and "tomato" in item.get("label", "").lower()]
                if tomato_results:
                    result = tomato_results
                    logger.info(f"Filtered to {len(tomato_results)} tomato-specific results")
            
            # Add disease descriptions and treatments
            result = enrich_disease_data(result)
            
            logger.info("Successfully processed disease detection")
            return {"prediction": result}
            
        except Exception as e:
            logger.error(f"Unhandled error in disease detection: {e}", exc_info=True)
            return {"error": f"Sorry, an error occurred: {str(e)}"}, 500

@disease_ns.route('/detect-file')
class DiseaseDetectionFileAPI(Resource):
    @disease_ns.doc('detect_disease_file')
    @disease_ns.expect(image_parser)
    @disease_ns.response(200, 'Success', disease_response)
    @disease_ns.response(202, 'Model Loading', loading_response)
    @disease_ns.response(400, 'Validation Error', error_response)
    @disease_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Detect diseases in tomato plant images (file upload)"""
        if not HUGGINGFACE_API_KEY:
            logger.error("HuggingFace API Key not configured")
            return {"error": "HuggingFace API Key not configured on server."}, 500
        
        try:
            # Process image from request
            try:
                if 'image' not in request.files:
                    return {"error": "No image file provided"}, 400
                    
                image_file = request.files['image']
                image_bytes = image_file.read()
                
                if not image_bytes:
                    return {"error": "Empty image file"}, 400
                
            except Exception as img_err:
                logger.error(f"Error processing image file: {img_err}")
                return {"error": str(img_err)}, 400
            
            # Call HuggingFace API
            huggingface_url = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
            
            # Set headers with content type
            content_type = detect_image_format(image_bytes)
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                "Content-Type": content_type
            }
            
            # Make API call
            try:
                response = call_huggingface_api(huggingface_url, headers, image_bytes)
                result = parse_huggingface_response(response)
                
                # Check if model is loading
                if isinstance(result, dict) and result.get("status") == "loading":
                    return result, 202
                    
            except (ConnectionError, ValueError) as api_err:
                return {"error": str(api_err)}, 500
            
            # Filter for tomato-specific results if possible
            if isinstance(result, list):
                tomato_results = [item for item in result if item.get("label") and "tomato" in item.get("label", "").lower()]
                if tomato_results:
                    result = tomato_results
                    logger.info(f"Filtered to {len(tomato_results)} tomato-specific results")
            
            # Add disease descriptions and treatments
            result = enrich_disease_data(result)
            
            logger.info("Successfully processed disease detection")
            return {"prediction": result}
            
        except Exception as e:
            logger.error(f"Unhandled error in disease detection: {e}", exc_info=True)
            return {"error": f"Sorry, an error occurred: {str(e)}"}, 500

@general_ns.route('/test')
class TestAPI(Resource):
    @general_ns.doc('test_api')
    @general_ns.response(200, 'Success', test_response)
    def get(self):
        """Test if the API is running properly"""
        return {"status": "success"}

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
    app.run(debug=True, port=5000) 