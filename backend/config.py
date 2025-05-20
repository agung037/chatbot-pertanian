import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5012))
    
    # API keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    # Model settings
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'tomato_disease.h5')
    LLM_MODEL = os.getenv('LLM_MODEL', 'llama3-8b-8192')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.7))
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', 1024))
    
    # CORS settings
    CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '*')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # In production, ensure secure settings
    def __init__(self):
        if not self.SECRET_KEY or self.SECRET_KEY == 'default-secret-key':
            raise ValueError("SECRET_KEY must be set for production")
        
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY must be set for production")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
    # Use mocked services for testing
    USE_MOCK_LLM = True
    USE_MOCK_MODEL = True


# Define configuration mapping
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# Default to development configuration if not specified
active_config = config_by_name.get(os.getenv('FLASK_ENV', 'development'), DevelopmentConfig) 