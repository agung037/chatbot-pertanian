from flask import Blueprint, request, jsonify, current_app, render_template
from services.service_registry import service_registry
import logging
from flask_restx import Resource

logger = logging.getLogger(__name__)

# Initialize blueprint
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Get Swagger resources when app context is available
def get_swagger_resources():
    """Get the Swagger resources from the app config."""
    return current_app.config.get('SWAGGER_RESOURCES', {})

# This function will be called after registering the blueprint
@chat_bp.record_once
def setup_swagger(state):
    app = state.app
    if 'SWAGGER_RESOURCES' in app.config:
        swagger_resources = app.config['SWAGGER_RESOURCES']
        ns = swagger_resources['namespaces']['chat']
        
        # Register API routes with the namespace
        
        @ns.route('')
        class ChatAPI(Resource):
            @ns.doc('chat_message')
            @ns.expect(swagger_resources['models']['chat_request'])
            @ns.response(200, 'Success', swagger_resources['models']['chat_response'])
            @ns.response(400, 'Validation Error', swagger_resources['models']['error_response'])
            @ns.response(503, 'Service Unavailable', swagger_resources['models']['error_response'])
            def post(self):
                """Send a message to the chatbot and get a response"""
                try:
                    # Get LLM service from registry
                    llm_service = service_registry.get_llm_service()
                    
                    # Check if the service is available
                    if not llm_service.is_available():
                        return {"error": "Chat service is not available. Check API keys."}, 503
                    
                    # Get the user message
                    data = request.json
                    if not data or 'message' not in data:
                        return {"error": "Message is required"}, 400
                        
                    user_message = data['message']
                    if not user_message.strip():
                        return {"error": "Message cannot be empty"}, 400
                    
                    # Log the user message
                    logger.info(f"Chat request received: {user_message[:50]}...")
                    
                    # Get response from the LLM
                    response = llm_service.get_chat_response(user_message)
                    
                    # Return the response
                    return {"response": response}, 200
                    
                except ValueError as ve:
                    logger.warning(f"Validation error in chat endpoint: {ve}")
                    return {"error": str(ve)}, 400
                    
                except Exception as e:
                    logger.error(f"Error in chat endpoint: {e}", exc_info=True)
                    return {"error": "An error occurred processing your request"}, 500
        
        @ns.route('/health')
        class ChatHealth(Resource):
            @ns.doc('chat_health')
            @ns.response(200, 'Success')
            @ns.response(500, 'Server Error', swagger_resources['models']['error_response'])
            def get(self):
                """Health check endpoint for the chat service"""
                try:
                    llm_service = service_registry.get_llm_service()
                    status = "available" if llm_service.is_available() else "unavailable"
                    return {
                        "status": status,
                        "service": "chat"
                    }, 200
                except Exception as e:
                    logger.error(f"Error in chat health check: {e}")
                    return {
                        "status": "error",
                        "service": "chat",
                        "error": str(e)
                    }, 500

# Keep the legacy route handler for serving the frontend page
@chat_bp.route('/ui', methods=['GET'])
def chat_page():
    """Serve the chat UI page."""
    return render_template('index.html') 