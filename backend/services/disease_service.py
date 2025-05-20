import logging
from flask import current_app
from models.plant_disease_model import PlantDiseaseModel
from utils.disease_data import enrich_disease_data
from utils.image_processing import process_image_data

logger = logging.getLogger(__name__)

class DiseaseService:
    """Service for disease detection and information."""
    
    def __init__(self, model_path=None):
        """Initialize the disease service with a model path."""
        try:
            if not model_path:
                model_path = current_app.config.get('MODEL_PATH')
                
            self.model = PlantDiseaseModel(model_path)
            logger.info("Disease service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize disease service: {e}", exc_info=True)
            self.model = None
    
    def is_available(self):
        """Check if the disease service is available."""
        return self.model is not None
    
    def process_image(self, image_data):
        """Process image data for disease detection."""
        if not image_data:
            raise ValueError("Image data cannot be empty")
            
        # Process the image data (base64 or raw bytes)
        if isinstance(image_data, str):
            # Handle base64 string
            return process_image_data(image_data)
        else:
            # Handle raw bytes
            return image_data
    
    def detect_disease(self, image_data):
        """Detect disease from image data."""
        if not self.is_available():
            raise ValueError("Disease service is not available")
        
        # Process the image
        image_bytes = self.process_image(image_data)
        
        # Make prediction
        result = self.model.predict(image_bytes)
        
        return result
    
    def detect_disease_with_info(self, image_data):
        """Detect disease and enrich with additional information."""
        result = self.detect_disease(image_data)
        
        # Enrich the result with additional information
        enriched_result = enrich_disease_data(result)
        
        return enriched_result 