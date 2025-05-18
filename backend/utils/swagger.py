from flask_restx import Api, Resource, fields, Namespace

# Create the API instance
api = Api(
    title="TomatBot API",
    version="1.0.0",
    description="API for TomatBot - A tomato cultivation chatbot with disease detection capabilities",
    doc="/docs",
)

# Create namespaces for different API groups
chat_ns = Namespace('chat', description='Chatbot operations')
disease_ns = Namespace('disease', description='Disease detection operations')
general_ns = Namespace('general', description='General operations')

# Register namespaces
api.add_namespace(chat_ns, path='/api/chat')
api.add_namespace(disease_ns, path='/api/disease')
api.add_namespace(general_ns, path='/api/general')

# Define models for request/response objects
chat_request = api.model('ChatRequest', {
    'message': fields.String(required=True, description='User message'),
})

chat_response = api.model('ChatResponse', {
    'response': fields.String(description='Bot response'),
})

error_response = api.model('ErrorResponse', {
    'error': fields.String(description='Error message'),
})

disease_info = api.model('DiseaseInfo', {
    'description': fields.String(description='Description of the disease'),
    'treatment': fields.String(description='Treatment suggestions'),
})

disease_prediction = api.model('DiseasePrediction', {
    'label': fields.String(description='Disease label'),
    'score': fields.Float(description='Confidence score'),
    'description': fields.String(description='Description of the disease'),
    'treatment': fields.String(description='Treatment suggestions'),
})

disease_response = api.model('DiseaseResponse', {
    'prediction': fields.List(fields.Nested(disease_prediction), description='Disease predictions'),
})

loading_response = api.model('LoadingResponse', {
    'status': fields.String(description='Status of the model'),
    'message': fields.String(description='Loading message'),
})

# Fix the parser configuration - don't add duplicate image arguments
image_parser = api.parser()
image_parser.add_argument('image', location='files', type='file', help='Image file')
# Use a different parser for JSON body
json_parser = api.parser()
json_parser.add_argument('image', location='json', type=str, help='Base64 encoded image')

test_response = api.model('TestResponse', {
    'status': fields.String(description='Status of API'),
}) 