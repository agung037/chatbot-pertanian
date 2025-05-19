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
from utils.model_prediction import (
    load_disease_detection_model, 
    preprocess_image, 
    predict_tomato_disease
)
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

# Load the local model
try:
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'plant_disease_model.h5')
    model = tf.keras.models.load_model(model_path)
    # Log model output shape
    output_shape = model.output_shape
    logger.info(f"Model loaded successfully. Output shape: {output_shape}")
except Exception as e:
    logger.error(f"Failed to load local model: {e}")
    model = None

def preprocess_image(image_bytes):
    """Preprocess image for model input"""
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Resize image to model's expected input size (224x224)
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise ValueError(f"Failed to preprocess image: {str(e)}")

def predict_disease(image_array):
    """Make prediction using the local model"""
    try:
        predictions = model.predict(image_array)
        # Log prediction shape and values
        logger.info(f"Prediction shape: {predictions.shape}")
        logger.info(f"Prediction values: {predictions[0]}")
        
        # Get the predicted class index
        predicted_class = np.argmax(predictions[0])
        # Get the confidence score
        confidence = float(predictions[0][predicted_class])
        
        logger.info(f"Predicted class index: {predicted_class}, Confidence: {confidence}")
        return predicted_class, confidence
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise ValueError(f"Failed to make prediction: {str(e)}")

# Define class names for tomato diseases
TOMATO_DISEASE_CLASSES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

# Map model output indices to tomato class indices
TOMATO_CLASS_MAPPING = {
    15: 0,  # Tomato___Bacterial_spot
    16: 1,  # Tomato___Early_blight
    17: 2,  # Tomato___Late_blight
    18: 3,  # Tomato___Leaf_Mold
    19: 4,  # Tomato___Septoria_leaf_spot
    20: 5,  # Tomato___Spider_mites
    21: 6,  # Tomato___Target_Spot
    22: 7,  # Tomato___Tomato_Yellow_Leaf_Curl_Virus
    23: 8,  # Tomato___Tomato_mosaic_virus
    24: 9,  # Tomato___healthy
    25: 0,  # Additional tomato classes that might be mapped to the same diseases
    26: 1,
    27: 2,
    28: 3,
    29: 4,
    30: 5,
    31: 6,
    32: 7,
    33: 8,
    34: 9,
    36: 9
}

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
    @disease_ns.response(400, 'Validation Error', error_response)
    @disease_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Detect diseases in tomato plant images using local model"""
        # Check if model is loaded
        if not model:
            logger.error("Disease detection model not loaded")
            return {"error": "Disease detection model not available."}, 500
        
        try:
            # Process image from request
            try:
                image_bytes = process_image_data(request.json if request.is_json else {})
            except ValueError as img_err:
                logger.error(f"Error processing image: {img_err}")
                return {"error": str(img_err)}, 400
            
            # Preprocess image for model input
            image_array = preprocess_image(image_bytes)
            
            # Predict tomato disease
            predicted_class_name, confidence = predict_tomato_disease(model, image_array)
            
            # Handle prediction results
            if not predicted_class_name:
                return {"error": "Unable to classify the image. Please provide a clear tomato plant image."}, 400
            
            # Create result with the predicted class
            result = [{
                "label": predicted_class_name,
                "score": confidence
            }]
            
            # Add disease descriptions and treatments
            result = enrich_disease_data(result)
            
            logger.info(f"Successfully processed tomato disease detection: {predicted_class_name}")
            return {"prediction": result}
            
        except Exception as e:
            logger.error(f"Unhandled error in disease detection: {e}", exc_info=True)
            return {"error": f"Sorry, an error occurred: {str(e)}"}, 500

@disease_ns.route('/detect-file')
class DiseaseDetectionFileAPI(Resource):
    @disease_ns.doc('detect_disease_file')
    @disease_ns.expect(image_parser)
    @disease_ns.response(200, 'Success', disease_response)
    @disease_ns.response(400, 'Validation Error', error_response)
    @disease_ns.response(500, 'Server Error', error_response)
    def post(self):
        """Detect diseases in tomato plant images using local model (file upload)"""
        # Check if model is loaded
        if not model:
            logger.error("Disease detection model not loaded")
            return {"error": "Disease detection model not available."}, 500
        
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
            
            # Preprocess image for model input
            image_array = preprocess_image(image_bytes)
            
            # Predict tomato disease
            predicted_class_name, confidence = predict_tomato_disease(model, image_array)
            
            # Handle prediction results
            if not predicted_class_name:
                return {"error": "Unable to classify the image. Please provide a clear tomato plant image."}, 400
            
            # Create result with the predicted class
            result = [{
                "label": predicted_class_name,
                "score": confidence
            }]
            
            # Add disease descriptions and treatments
            result = enrich_disease_data(result)
            
            logger.info(f"Successfully processed tomato disease detection: {predicted_class_name}")
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