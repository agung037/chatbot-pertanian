import base64
import io
import logging
from PIL import Image
from flask import request

logger = logging.getLogger(__name__)

def process_image_data(request_data):
    """Process image data from request (file upload or base64)"""
    if 'image' in request.files:
        logger.info("Processing image from file upload")
        image_file = request.files['image']
        image_bytes = image_file.read()
        logger.info(f"Successfully read image file, size: {len(image_bytes)} bytes")
        return image_bytes
    
    elif 'image' in request_data:
        logger.info("Processing image from base64 data")
        image_data = request_data.get('image', '')
        if not image_data:
            raise ValueError("Empty image data")
            
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
            
        try:
            image_bytes = base64.b64decode(image_data)
            if not image_bytes:
                raise ValueError("Invalid base64 image data")
            logger.info(f"Successfully decoded base64 image, size: {len(image_bytes)} bytes")
            return image_bytes
        except Exception as decode_err:
            logger.error(f"Error decoding base64 image: {decode_err}")
            raise ValueError(f"Failed to decode image: {str(decode_err)}")
    
    raise ValueError("No image provided in request")

def detect_image_format(image_bytes):
    """Detect image format and return appropriate content type"""
    img_io = io.BytesIO(image_bytes)
    try:
        image = Image.open(img_io)
        image_format = image.format.lower() if image.format else "jpeg"
        logger.info(f"Detected image format: {image_format}")
        
        # Map image format to content type
        content_types = {
            "jpeg": "image/jpeg",
            "jpg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "bmp": "image/bmp"
        }
        
        return content_types.get(image_format, "image/jpeg")
    except Exception as img_err:
        logger.error(f"Error determining image format: {img_err}")
        return "image/jpeg"  # Default to jpeg if can't determine 