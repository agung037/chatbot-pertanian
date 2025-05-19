import os
import logging
import numpy as np
import tensorflow as tf
from PIL import Image
import io

# Configure logging
logger = logging.getLogger(__name__)

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
    34: 9
}

def load_disease_detection_model(model_path):
    """
    Load a TensorFlow/Keras model for disease detection.
    
    Args:
        model_path (str): Path to the .h5 model file
    
    Returns:
        tf.keras.Model: Loaded model or None if loading fails
    """
    try:
        model = tf.keras.models.load_model(model_path)
        logger.info(f"Successfully loaded disease detection model from {model_path}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from {model_path}: {e}")
        return None

def preprocess_image(image_bytes, target_size=(224, 224)):
    """
    Preprocess an image for model prediction.
    
    Args:
        image_bytes (bytes): Image data in bytes
        target_size (tuple): Target image size for resizing
    
    Returns:
        numpy.ndarray: Preprocessed image array
    """
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Resize image to target size
        image = image.resize(target_size)
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise ValueError(f"Failed to preprocess image: {str(e)}")

def predict_tomato_disease(model, image_array):
    """
    Predict tomato disease from an image.
    
    Args:
        model (tf.keras.Model): Loaded disease detection model
        image_array (numpy.ndarray): Preprocessed image array
    
    Returns:
        tuple: (predicted class name, confidence score)
    """
    try:
        # Make prediction
        predictions = model.predict(image_array)
        
        # Log prediction details for debugging
        logger.info(f"Prediction shape: {predictions.shape}")
        logger.info(f"Prediction values: {predictions[0]}")
        
        # Get the predicted class index
        predicted_class = np.argmax(predictions[0])
        # Get the confidence score
        confidence = float(predictions[0][predicted_class])
        
        logger.info(f"Predicted class index: {predicted_class}, Confidence: {confidence}")
        
        # Check if the prediction is a tomato-related class
        if predicted_class not in TOMATO_CLASS_MAPPING:
            logger.warning(f"Non-tomato prediction detected: class {predicted_class}")
            return None, None
        
        # Map to tomato class index
        tomato_class_index = TOMATO_CLASS_MAPPING[predicted_class]
        predicted_class_name = TOMATO_DISEASE_CLASSES[tomato_class_index]
        
        return predicted_class_name, confidence
    
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise ValueError(f"Failed to make prediction: {str(e)}") 