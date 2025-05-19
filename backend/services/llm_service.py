import logging
from groq import Groq
from flask import current_app

from utils.llm import create_chat_messages, create_disease_info_prompt

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLM APIs like Groq."""
    
    def __init__(self, api_key=None):
        """Initialize the LLM service with the provided API key."""
        try:
            if not api_key:
                api_key = current_app.config.get('GROQ_API_KEY')
                
            if not api_key:
                logger.warning("No API key provided for LLM service")
                self.client = None
            else:
                self.client = Groq(api_key=api_key)
                logger.info("LLM service initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {e}", exc_info=True)
            self.client = None
    
    def is_available(self):
        """Check if the LLM service is available."""
        return self.client is not None
    
    def get_chat_response(self, user_message):
        """Get a response from the LLM for a chat message."""
        if not self.is_available():
            raise ValueError("LLM service is not available")
        
        if not user_message:
            raise ValueError("User message cannot be empty")
        
        try:
            # Create the chat messages
            messages = create_chat_messages(user_message)
            
            # Get the model settings from the app config
            model = current_app.config.get('LLM_MODEL', 'llama3-8b-8192')
            temperature = current_app.config.get('LLM_TEMPERATURE', 0.7)
            max_tokens = current_app.config.get('LLM_MAX_TOKENS', 1024)
            
            # Send request to the LLM API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stop=None,
                stream=False,
            )
            
            # Extract the response
            response = chat_completion.choices[0].message.content
            logger.info(f"Generated chat response: {response[:50]}...")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating chat response: {e}", exc_info=True)
            raise
    
    def get_disease_info(self, disease_name):
        """Get detailed information about a disease from the LLM."""
        if not self.is_available():
            raise ValueError("LLM service is not available")
        
        if not disease_name:
            raise ValueError("Disease name cannot be empty")
        
        try:
            # Create the disease info prompt
            messages = create_disease_info_prompt(disease_name)
            
            # Get the model settings from the app config
            model = current_app.config.get('LLM_MODEL', 'llama3-8b-8192')
            temperature = current_app.config.get('LLM_TEMPERATURE', 0.7)
            max_tokens = current_app.config.get('LLM_MAX_TOKENS', 1024)
            
            # Send request to the LLM API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stop=None,
                stream=False,
            )
            
            # Extract the response
            response = chat_completion.choices[0].message.content
            logger.info(f"Generated disease info for {disease_name}: {response[:50]}...")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating disease info: {e}", exc_info=True)
            raise 