import logging

logger = logging.getLogger(__name__)

# Disease information database
DISEASE_INFO = {
    "early blight": {
        "description": "Early blight is characterized by brown spots with concentric rings that grow together.",
        "treatment": "Remove affected leaves, improve air circulation, and apply appropriate fungicides."
    },
    "late blight": {
        "description": "Late blight appears as dark, water-soaked spots with white fungal growth on undersides.",
        "treatment": "Remove infected plants, ensure good drainage, and apply copper-based fungicides."
    },
    "leaf mold": {
        "description": "Leaf mold shows as yellow spots on upper leaf surfaces with gray-brown growths underneath.",
        "treatment": "Improve ventilation, reduce humidity, and apply suitable fungicides."
    },
    "healthy": {
        "description": "This plant appears healthy with no visible disease symptoms.",
        "treatment": "Continue regular care and monitoring."
    }
}

def enrich_disease_data(predictions):
    """Add description and treatment data to disease predictions"""
    if not isinstance(predictions, list):
        return predictions
        
    for item in predictions:
        label = item.get("label")
        if not label:
            continue
            
        disease = label.lower()
        
        # Add disease info from database
        for disease_key, info in DISEASE_INFO.items():
            if disease_key in disease:
                item["description"] = info["description"]
                item["treatment"] = info["treatment"]
                break
    
    return predictions 