#!/usr/bin/env python
"""
This script generates an OpenAPI specification file from the AgroBot API
and saves it to the frontend directory for easy access.
"""

import json
import os
import sys
import logging

# Add parent directory to path so we can import from our app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_openapi_spec():
    """Generate OpenAPI spec from the Flask app and save it to a file."""
    try:
        # Import the app and create an instance
        from app import create_app
        app = create_app()
        
        # Get API instance to generate spec
        api = None
        for extension in app.extensions.values():
            if hasattr(extension, 'specs'):
                api = extension
                break
        
        if not api:
            logger.error("Could not find Flask-RESTX API instance")
            return False
            
        # Get the OpenAPI spec
        with app.app_context():
            spec = api.__schema__
            
        # Locations to save the spec file
        locations = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'openapi.json'),
            os.path.join(os.path.dirname(__file__), '..', 'static', 'openapi.json')
        ]
        
        # Save the spec to files
        for location in locations:
            os.makedirs(os.path.dirname(location), exist_ok=True)
            with open(location, 'w') as f:
                json.dump(spec, f, indent=2)
            logger.info(f"OpenAPI spec saved to {location}")
            
        return True
        
    except Exception as e:
        logger.error(f"Error generating OpenAPI spec: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    if generate_openapi_spec():
        logger.info("Successfully generated OpenAPI specification")
        sys.exit(0)
    else:
        logger.error("Failed to generate OpenAPI specification")
        sys.exit(1) 