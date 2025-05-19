import logging
from flask import current_app
from services.llm_service import LLMService
from services.disease_service import DiseaseService

logger = logging.getLogger(__name__)

class ServiceRegistry:
    """
    A registry for managing services used by the application.
    
    This class follows the Singleton pattern to ensure that services
    are initialized only once and shared across the application.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._services = {}
            self._initialized = True
            logger.info("Service registry initialized")
    
    def initialize_services(self, app=None):
        """Initialize all services with the application context."""
        try:
            # Initialize LLM service
            self._services['llm'] = LLMService(
                api_key=current_app.config.get('GROQ_API_KEY') if app else None
            )
            
            # Initialize disease service
            self._services['disease'] = DiseaseService(
                model_path=current_app.config.get('MODEL_PATH') if app else None
            )
            
            logger.info("All services initialized")
            return True
        except Exception as e:
            logger.error(f"Error initializing services: {e}", exc_info=True)
            return False
    
    def get_service(self, service_name):
        """Get a service by name."""
        if service_name not in self._services:
            raise ValueError(f"Service '{service_name}' not found")
        return self._services[service_name]
    
    def get_llm_service(self):
        """Get the LLM service."""
        if 'llm' not in self._services:
            self._services['llm'] = LLMService()
        return self._services['llm']
    
    def get_disease_service(self):
        """Get the disease service."""
        if 'disease' not in self._services:
            self._services['disease'] = DiseaseService()
        return self._services['disease']
    
    def health_check(self):
        """Check the health of all services."""
        health_status = {}
        
        # Check LLM service
        llm_service = self.get_llm_service()
        health_status['llm'] = {
            "status": "available" if llm_service.is_available() else "unavailable"
        }
        
        # Check disease service
        disease_service = self.get_disease_service()
        health_status['disease'] = {
            "status": "available" if disease_service.is_available() else "unavailable"
        }
        
        # Overall health
        all_available = all(service["status"] == "available" for service in health_status.values())
        health_status['overall'] = "healthy" if all_available else "degraded"
        
        return health_status
    
    def shutdown(self):
        """Clean up services when shutting down."""
        self._services.clear()
        logger.info("All services shut down")

# Export a singleton instance
service_registry = ServiceRegistry() 