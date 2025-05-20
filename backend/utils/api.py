# import logging
# import requests

# logger = logging.getLogger(__name__)

# def call_huggingface_api(url, headers, image_bytes, timeout=30):
#     """Make a request to the HuggingFace API with proper error handling"""
#     try:
#         response = requests.post(
#             url,
#             headers=headers,
#             data=image_bytes,
#             timeout=timeout
#         )
#         logger.info(f"HuggingFace API response status: {response.status_code}")
#         return response
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"Failed to connect to HuggingFace API: {req_err}", exc_info=True)
#         raise ConnectionError(f"Failed to connect to HuggingFace API: {str(req_err)}")

# def parse_huggingface_response(response):
#     """Parse the HuggingFace API response with error handling"""
#     if not response.content:
#         logger.error("Empty response from HuggingFace API")
#         raise ValueError("Empty response from HuggingFace API")
        
#     try:
#         result = response.json()
#         logger.info(f"Received response from HuggingFace")
        
#         # Check for model errors
#         if isinstance(result, dict) and 'error' in result:
#             error_msg = result['error']
#             logger.error(f"HuggingFace model returned an error: {error_msg}")
            
#             # Check if model is loading
#             if error_msg.startswith("Model"):
#                 return {"status": "loading", "message": error_msg}
                
#             raise ValueError(f"Model error: {error_msg}")
            
#         return result
#     except ValueError as json_err:
#         logger.error(f"Invalid JSON response: {json_err}", exc_info=True)
#         raise ValueError(f"Invalid response from HuggingFace API") 