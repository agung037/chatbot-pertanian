from flask_restx import Api, Namespace, fields
import os

def create_swagger_api(app=None):
    """Create and configure the Swagger API instance.
    
    This function centralizes the configuration of the Swagger API, making it
    easier to integrate with the Flask application factory pattern.
    """
    # Create the API instance
    api = Api(
        title="AgroBot API",
        version="1.0.0",
        description="API for AgroBot - A tomato cultivation chatbot with disease detection capabilities",
        doc="/docs",  # Swagger UI will be available at this endpoint
    )
    
    # Create namespaces for different API groups
    chat_ns = Namespace('chat', description='Chatbot operations')
    disease_ns = Namespace('disease', description='Disease detection operations')
    general_ns = Namespace('general', description='General operations')
    
    # Register namespaces with prefixes
    api.add_namespace(chat_ns, path='/api/chat')
    api.add_namespace(disease_ns, path='/api/disease')
    api.add_namespace(general_ns, path='/api')
    
    # Define models for request/response objects
    
    # Chat models
    chat_request = api.model('ChatRequest', {
        'message': fields.String(required=True, description='User message'),
    })
    
    chat_response = api.model('ChatResponse', {
        'response': fields.String(description='Bot response'),
    })
    
    # General models
    error_response = api.model('ErrorResponse', {
        'error': fields.String(description='Error message'),
    })
    
    test_response = api.model('TestResponse', {
        'status': fields.String(description='Status of API'),
        'message': fields.String(description='Status message'),
    })
    
    health_response = api.model('HealthResponse', {
        'status': fields.String(description='Health status of the API'),
        'services': fields.Raw(description='Status of individual services'),
        'version': fields.String(description='API version'),
        'environment': fields.String(description='Deployment environment'),
    })
    
    # Disease models
    disease_info = api.model('DiseaseInfo', {
        'description': fields.String(description='Description of the disease'),
        'treatment': fields.String(description='Treatment suggestions'),
    })
    
    disease_prediction = api.model('DiseasePrediction', {
        'prediction': fields.String(description='Disease name'),
        'confidence': fields.Float(description='Confidence score'),
        'llmInfo': fields.String(description='Detailed disease information from LLM'),
    })
    
    disease_response = api.model('DiseaseResponse', {
        'prediction': fields.String(description='Disease name'),
        'confidence': fields.Float(description='Confidence score'),
        'llmInfo': fields.String(description='Detailed disease information from LLM'),
    })
    
    loading_response = api.model('LoadingResponse', {
        'status': fields.String(description='Status of the model'),
        'message': fields.String(description='Loading message'),
    })
    
    # File upload parsers
    image_parser = api.parser()
    image_parser.add_argument('image', location='files', type='file', help='Image file')
    
    # Base64 image parser
    json_parser = api.parser()
    json_parser.add_argument('image', location='json', type=str, help='Base64 encoded image')
    json_parser.add_argument('requestLlmInfo', location='json', type=bool, help='Whether to request LLM information')
    
    return api, {
        'namespaces': {
            'chat': chat_ns,
            'disease': disease_ns, 
            'general': general_ns
        },
        'models': {
            'chat_request': chat_request,
            'chat_response': chat_response,
            'error_response': error_response,
            'test_response': test_response,
            'health_response': health_response,
            'disease_info': disease_info,
            'disease_prediction': disease_prediction,
            'disease_response': disease_response,
            'loading_response': loading_response
        },
        'parsers': {
            'image_parser': image_parser,
            'json_parser': json_parser
        }
    } 