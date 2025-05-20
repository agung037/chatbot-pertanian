import tensorflow as tf
import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class PlantDiseaseModel:
    def __init__(self, model_path):
        """Initialize the plant disease model"""
        try:
            self.model = tf.keras.models.load_model(model_path)
            self.class_names = [
                "Tomato_Bacterial_spot",
                "Tomato_Early_blight",
                "Tomato_Late_blight",
                "Tomato_Leaf_Mold",
                "Tomato_Septoria_leaf_spot",
                "Tomato_Spider_mites_Two_spotted_spider_mite",
                "Tomato__Target_Spot",
                "Tomato__Tomato_YellowLeaf__Curl_Virus",
                "Tomato__Tomato_mosaic_virus",
                "Tomato_healthy"
            ]
            logger.info("Plant disease model loaded successfully")
            # Log model output shape for debugging
            output_shape = self.model.output_shape
            logger.info(f"Model output shape: {output_shape}")
            logger.info(f"Number of classes in model: {len(self.class_names)}")
        except Exception as e:
            logger.error(f"Failed to load plant disease model: {str(e)}", exc_info=True)
            raise

    def preprocess_image(self, image_bytes):
        """Preprocess the image for model prediction"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image to match model's expected input size (256x256)
            image = image.resize((256, 256))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
        except Exception as e:
            logger.error(f"Failed to preprocess image: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to preprocess image: {str(e)}")

    def predict(self, image_bytes):
        """Make prediction on the input image"""
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_bytes)
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            
            # Get the predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Log prediction details for debugging
            logger.info(f"Raw predictions shape: {predictions.shape}")
            logger.info(f"Predicted class index: {predicted_class_idx}")
            logger.info(f"Confidence: {confidence}")
            
            # Validate the predicted class index
            if predicted_class_idx >= len(self.class_names):
                logger.warning(f"Predicted class index {predicted_class_idx} is out of range. Max index is {len(self.class_names)-1}")
                return {
                    "prediction": "Unknown",
                    "confidence": confidence,
                    "error": "Model prediction is outside known classes"
                }
            
            predicted_class = self.class_names[predicted_class_idx]
            
            return {
                "prediction": predicted_class,
                "confidence": confidence
            }
        except Exception as e:
            logger.error(f"Failed to make prediction: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to make prediction: {str(e)}") 