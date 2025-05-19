#!/usr/bin/env python
"""
This script verifies that the Swagger API documentation is accessible and contains operations.
It connects to a running AgroBot API instance and checks the OpenAPI specification.
"""

import json
import requests
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_swagger_api(base_url="http://localhost:5012"):
    """
    Verify that the Swagger API documentation is working correctly.
    
    Args:
        base_url (str): The base URL of the AgroBot API
        
    Returns:
        bool: True if verification passed, False otherwise
    """
    # Check if the Swagger UI is accessible
    try:
        logger.info(f"Checking Swagger UI at {base_url}/docs...")
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code != 200:
            logger.error(f"Swagger UI not accessible. Status code: {response.status_code}")
            return False
        logger.info("Swagger UI is accessible")
        
        # Check if the OpenAPI specification is accessible
        logger.info(f"Checking OpenAPI specification at {base_url}/swagger.json...")
        response = requests.get(f"{base_url}/swagger.json", timeout=5)
        if response.status_code != 200:
            logger.error(f"OpenAPI spec not accessible. Status code: {response.status_code}")
            return False
        
        # Parse the OpenAPI spec
        try:
            spec = response.json()
            
            # Check if there are paths in the spec
            if 'paths' not in spec or not spec['paths']:
                logger.error("No paths found in OpenAPI spec")
                return False
                
            # Count the number of operations
            operation_count = 0
            for path, methods in spec['paths'].items():
                for method in methods:
                    if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                        operation_count += 1
                        
            if operation_count == 0:
                logger.error("No operations defined in OpenAPI spec")
                return False
                
            logger.info(f"Found {operation_count} API operations in {len(spec['paths'])} paths")
            
            # Check if models are defined
            if 'definitions' in spec and spec['definitions']:
                model_count = len(spec['definitions'])
                logger.info(f"Found {model_count} model definitions")
            elif 'components' in spec and 'schemas' in spec['components']:
                model_count = len(spec['components']['schemas'])
                logger.info(f"Found {model_count} model schemas")
            else:
                logger.warning("No model definitions found in OpenAPI spec")
            
            return True
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in OpenAPI spec")
            return False
            
    except requests.RequestException as e:
        logger.error(f"Error connecting to API: {e}")
        return False

if __name__ == "__main__":
    # Get base URL from command line argument if provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5012"
    
    if verify_swagger_api(base_url):
        logger.info("Swagger API verification passed!")
        sys.exit(0)
    else:
        logger.error("Swagger API verification failed!")
        sys.exit(1) 