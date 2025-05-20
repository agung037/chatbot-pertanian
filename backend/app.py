import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Import routes and blueprints
from routes.chat import chat_bp
from routes.disease import disease_bp
from routes.general import general_bp

# Import config and service registry
from config import Config, config_by_name
from services.service_registry import service_registry
from utils.swagger import create_swagger_api

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app(config_class=None):
    """Application factory function to create and configure the Flask app."""
    # Load environment variables
    load_dotenv()
    
    # Set config class based on environment if not provided
    if config_class is None:
        env = os.getenv('FLASK_ENV', 'development')
        config_class = config_by_name[env]
        logger.info(f"Using {env} configuration")
    
    # Initialize Flask app
    app = Flask(__name__, 
                template_folder='../frontend', 
                static_folder='../frontend',
                static_url_path='')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize Swagger documentation
    api, swagger_resources = create_swagger_api()
    api.init_app(app)
    
    # Store swagger resources for access in routes
    app.config['SWAGGER_RESOURCES'] = swagger_resources
    
    # Register blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(disease_bp)
    app.register_blueprint(general_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Initialize services with app context
    with app.app_context():
        service_registry.initialize_services(app)
    
    # Register shutdown handler
    register_teardown_handlers(app)
    
    # Add a route that redirects root to Swagger UI
    @app.route('/swagger')
    def swagger_redirect():
        return app.redirect('/docs')
    
    # Add a route for API documentation page
    @app.route('/api-docs')
    def api_docs():
        return send_from_directory('../frontend', 'api_docs.html')
    
    return app

def register_error_handlers(app):
    """Register error handlers for the application."""
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

def register_teardown_handlers(app):
    """Register teardown handlers for the application."""
    @app.teardown_appcontext
    def shutdown_services(exception=None):
        service_registry.shutdown()

if __name__ == '__main__':
    # Create app
    app = create_app()
    
    # Run the app
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    ) 