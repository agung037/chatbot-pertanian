from flask import Blueprint, request, jsonify, current_app
from services.service_registry import service_registry
import logging
from flask_restx import Resource

logger = logging.getLogger(__name__)

# Initialize blueprint
disease_bp = Blueprint('disease', __name__, url_prefix='/api/disease')

# Get Swagger resources when app context is available
def get_swagger_resources():
    """Get the Swagger resources from the app config."""
    return current_app.config.get('SWAGGER_RESOURCES', {})

# This function will be called after registering the blueprint
@disease_bp.record_once
def setup_swagger(state):
    app = state.app
    if 'SWAGGER_RESOURCES' in app.config:
        swagger_resources = app.config['SWAGGER_RESOURCES']
        ns = swagger_resources['namespaces']['disease']
        
        # Register API routes with the namespace
        
        @ns.route('/detect')
        class DiseaseDetect(Resource):
            @ns.doc('detect_disease')
            @ns.expect(swagger_resources['parsers']['json_parser'])
            @ns.response(200, 'Success', swagger_resources['models']['disease_response'])
            @ns.response(400, 'Validation Error', swagger_resources['models']['error_response'])
            @ns.response(503, 'Service Unavailable', swagger_resources['models']['error_response'])
            def post(self):
                """Detect disease using base64 encoded image"""
                try:
                    # Get disease service from registry
                    disease_service = service_registry.get_disease_service()
                    
                    # Check if the service is available
                    if not disease_service.is_available():
                        return {"error": "Disease detection service is not available"}, 503
                    
                    # Get the image data
                    data = request.json
                    if not data or 'image' not in data:
                        return {"error": "Image data is required"}, 400
                        
                    image_data = data['image']
                    
                    # Process the image and detect disease
                    result = disease_service.detect_disease(image_data)
                    
                    # Check if LLM info was requested
                    if data.get('requestLlmInfo', False):
                        # Try to get LLM info if a disease was detected
                        if result and 'prediction' in result:
                            try:
                                # Get LLM service from registry
                                llm_service = service_registry.get_llm_service()
                                
                                if llm_service.is_available():
                                    # Get disease info
                                    disease_name = result['prediction']
                                    llm_info = llm_service.get_disease_info(disease_name)
                                    
                                    # Add to result
                                    result['llmInfo'] = llm_info
                                else:
                                    logger.warning("LLM service not available for disease info")
                            except Exception as llm_err:
                                logger.error(f"Error getting LLM disease info: {llm_err}")
                                result['llmInfoError'] = "Failed to get disease information"
                    
                    return result, 200
                    
                except ValueError as ve:
                    logger.warning(f"Validation error in disease detection: {ve}")
                    return {"error": str(ve)}, 400
                    
                except Exception as e:
                    logger.error(f"Error in disease detection: {e}", exc_info=True)
                    return {"error": "An error occurred processing your request"}, 500
        
        @ns.route('/detect-file')
        class DiseaseDetectFile(Resource):
            @ns.doc('detect_disease_file')
            @ns.expect(swagger_resources['parsers']['image_parser'])
            @ns.response(200, 'Success', swagger_resources['models']['disease_response'])
            @ns.response(400, 'Validation Error', swagger_resources['models']['error_response'])
            @ns.response(503, 'Service Unavailable', swagger_resources['models']['error_response'])
            def post(self):
                """Detect disease using uploaded image file"""
                try:
                    # Get disease service from registry
                    disease_service = service_registry.get_disease_service()
                    
                    # Check if the service is available
                    if not disease_service.is_available():
                        return {"error": "Disease detection service is not available"}, 503
                    
                    # Get the image file
                    if 'image' not in request.files:
                        return {"error": "Image file is required"}, 400
                        
                    image_file = request.files['image']
                    if not image_file:
                        return {"error": "Empty image file"}, 400
                        
                    # Read image bytes
                    image_bytes = image_file.read()
                    if not image_bytes:
                        return {"error": "Could not read image file"}, 400
                    
                    # Process the image and detect disease
                    result = disease_service.detect_disease_with_info(image_bytes)
                    
                    return result, 200
                    
                except ValueError as ve:
                    logger.warning(f"Validation error in file detection: {ve}")
                    return {"error": str(ve)}, 400
                    
                except Exception as e:
                    logger.error(f"Error in file detection: {e}", exc_info=True)
                    return {"error": "An error occurred processing your request"}, 500
        
        @ns.route('/health')
        class DiseaseHealth(Resource):
            @ns.doc('disease_health')
            @ns.response(200, 'Success')
            @ns.response(500, 'Server Error', swagger_resources['models']['error_response'])
            def get(self):
                """Health check endpoint for the disease detection service"""
                try:
                    disease_service = service_registry.get_disease_service()
                    status = "available" if disease_service.is_available() else "unavailable"
                    return {
                        "status": status,
                        "service": "disease_detection"
                    }, 200
                except Exception as e:
                    logger.error(f"Error in disease service health check: {e}")
                    return {
                        "status": "error",
                        "service": "disease_detection",
                        "error": str(e)
                    }, 500
        
        @ns.route('')
        class LegacyDetect(Resource):
            @ns.doc('legacy_detect')
            @ns.response(200, 'Success', swagger_resources['models']['disease_response'])
            @ns.response(400, 'Validation Error', swagger_resources['models']['error_response'])
            @ns.response(503, 'Service Unavailable', swagger_resources['models']['error_response'])
            def post(self):
                """Legacy endpoint for disease detection (redirects to the proper endpoint)"""
                if request.files and 'image' in request.files:
                    return DiseaseDetectFile().post()
                return DiseaseDetect().post() 