from flask import Blueprint, jsonify, render_template, current_app
from services.service_registry import service_registry
import logging
import os
from flask_restx import Resource

logger = logging.getLogger(__name__)

# Initialize blueprint
general_bp = Blueprint('general', __name__)

# Get Swagger resources when app context is available
def get_swagger_resources():
    """Get the Swagger resources from the app config."""
    return current_app.config.get('SWAGGER_RESOURCES', {})

# This function will be called after registering the blueprint
@general_bp.record_once
def setup_swagger(state):
    app = state.app
    if 'SWAGGER_RESOURCES' in app.config:
        swagger_resources = app.config['SWAGGER_RESOURCES']
        ns = swagger_resources['namespaces']['general']
        
        # Register API routes with the namespace
        
        @ns.route('/health')
        class HealthCheck(Resource):
            @ns.doc('health_check')
            @ns.response(200, 'Success', swagger_resources['models']['health_response'])
            @ns.response(500, 'Server Error', swagger_resources['models']['error_response'])
            def get(self):
                """Health check endpoint for the whole API"""
                try:
                    # Get health status from service registry
                    health_status = service_registry.health_check()
                    
                    # Add version and environment info
                    response = {
                        "status": health_status['overall'],
                        "services": {
                            "llm": health_status['llm']['status'],
                            "disease_detection": health_status['disease']['status']
                        },
                        "version": current_app.config.get('VERSION', '1.0.0'),
                        "environment": os.getenv('FLASK_ENV', 'development')
                    }
                    
                    return response, 200
                except Exception as e:
                    logger.error(f"Error in health check: {e}")
                    return {
                        "status": "error",
                        "error": str(e)
                    }, 500
        
        @ns.route('/test')
        class TestAPI(Resource):
            @ns.doc('test_api')
            @ns.response(200, 'Success', swagger_resources['models']['test_response'])
            def get(self):
                """Simple test endpoint"""
                return {
                    "status": "success",
                    "message": "API is running"
                }, 200

# Legacy route handler for the UI
@general_bp.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

# Legacy endpoints for backward compatibility
@general_bp.route('/test')
def legacy_test():
    """Legacy test endpoint."""
    try:
        swagger_resources = get_swagger_resources()
        if swagger_resources and 'namespaces' in swagger_resources:
            # Use the Resource class if available
            return TestAPI().get()
        # Fallback
        return jsonify({
            "status": "success",
            "message": "API is running"
        }), 200
    except Exception as e:
        logger.error(f"Error in legacy test endpoint: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@general_bp.route('/api/health')
def health_check_legacy():
    """Legacy health check endpoint."""
    try:
        swagger_resources = get_swagger_resources()
        if swagger_resources and 'namespaces' in swagger_resources:
            # Use the Resource class if available
            return HealthCheck().get()
        
        # Fallback implementation
        health_status = service_registry.health_check()
        return jsonify({
            "status": health_status['overall'],
            "services": {
                "llm": health_status['llm']['status'],
                "disease_detection": health_status['disease']['status']
            },
            "version": current_app.config.get('VERSION', '1.0.0'),
            "environment": os.getenv('FLASK_ENV', 'development')
        }), 200
    except Exception as e:
        logger.error(f"Error in legacy health check: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# Error handlers
@general_bp.app_errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404

@general_bp.app_errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405

@general_bp.app_errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500 