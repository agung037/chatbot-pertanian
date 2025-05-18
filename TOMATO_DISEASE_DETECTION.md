# Tomato Disease Detection Feature

This feature allows users to upload images of tomato leaves and detect diseases using machine learning via the Hugging Face API.

## Setup Instructions

1. **Get a Hugging Face API Token**:
   - Create an account at [Hugging Face](https://huggingface.co/)
   - Go to your profile settings and create an API token with read access
   - Copy the token for the next step

2. **Set up Environment Variables**:
   - Create a `.env` file in the `backend` directory (or copy and rename `.env.example` if it exists)
   - Add your Hugging Face API token:
     ```
     HUGGINGFACE_API_KEY=your_huggingface_api_token_here
     GROQ_API_KEY=your_existing_groq_api_key_here
     ```

3. **Install Dependencies**:
   - Navigate to the backend directory
   - Run `pip install -r requirements.txt`

4. **Start the Application**:
   - Run the Flask app with `python app.py`
   - The server will start on port 5000

## How to Use

1. Navigate to the disease detection page in the web interface
2. Upload a tomato leaf image by clicking "Choose Image" or by dragging and dropping
3. Click "Detect Disease" to analyze the image
4. View the results, which will show:
   - Detected disease(s) with confidence percentages
   - Description of the disease
   - Treatment recommendations

## How It Works

- The frontend collects the image and sends it to the Flask backend
- The backend converts the image and sends it to a pre-trained tomato disease classification model on Hugging Face (Sakil/PlantDiseaseDetect)
- The model identifies any diseases present in the image
- The backend adds additional treatment information to the results
- The results are displayed in a user-friendly format on the frontend

## Supported Diseases

The model can detect various tomato leaf diseases, including:
- Early Blight
- Late Blight
- Leaf Mold
- And others depending on the model's capabilities

## Troubleshooting

- If you see a "Model is loading" message, wait a few seconds and try again
- Ensure your images are clear and well-lit for the best results
- Use only tomato plant images for accurate results
- Make sure your Hugging Face API token is valid and has appropriate permissions 