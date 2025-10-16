import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Flask app and Gemini API
app = Flask(__name__)

# They are crucial setting for the app and its performance
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]


try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    # Initialize the model with the safety settings
    model = genai.GenerativeModel('gemini-2.5-flash', safety_settings=safety_settings)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    # Handle the error gracefully, maybe exit or use a fallback
    model = None


# Function to call the LLM
def call_gemini(symptoms):
    """
    Constructs a detailed prompt and calls the Gemini API.
    Includes a strong educational disclaimer.
    """
    if not model:
        return "Error: The generative model is not configured. Please check the API key."

    # This prompt is engineered to be clear, safe, and responsible.
    prompt = f"""
    **SYSTEM PROMPT**
    You are a helpful AI assistant providing health information for educational purposes only.
    You are NOT a medical professional. Your suggestions are not a substitute for professional medical advice, diagnosis, or treatment.

    **TASK**
    Based on the symptoms provided by the user, you must perform the following steps:
    1.  Analyze the symptoms.
    2.  Suggest a few possible, common conditions that might be associated with these symptoms. Do not provide an exhaustive list.
    3.  Recommend clear, safe, and responsible next steps. Prioritize consulting a healthcare professional.
    4.  **Crucially, you MUST include the full disclaimer provided below at the end of your response.**

    **USER SYMPTOMS**
    "{symptoms}"

    **RESPONSE STRUCTURE**
    Your response should be formatted clearly, for example:

    **Possible Conditions:**
    * [Condition 1]: [Brief, high-level educational description]
    * [Condition 2]: [Brief, high-level educational description]

    **Recommended Next Steps:**
    * **Consult a Healthcare Professional:** It is essential to speak with a doctor or other qualified healthcare provider to get an accurate diagnosis.
    * [Other safe, general advice, e.g., "Rest and stay hydrated."]
    * [Advice on when to seek immediate medical attention, if applicable, e.g., "If you experience difficulty breathing, chest pain, or a high fever, seek medical help immediately."]

    ---
    **IMPORTANT DISCLAIMER:** This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read here.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Handle potential API errors (e.g., network issues, invalid key)
        print(f"An error occurred while calling the Gemini API: {e}")
        return "Sorry, there was an error processing your request. Please try again later."

#Define Home Page Route
@app.route('/')
def home():
    return render_template('index.html')

# Define the API endpoint
@app.route('/check_symptoms', methods=['POST'])
def check_symptoms():
    """
    API endpoint to receive symptoms and return potential conditions and advice.
    """
    # Get the symptom text from the incoming request
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({"error": "No symptoms provided. Please send a JSON object with a 'symptoms' key."}), 400

    symptoms = data['symptoms']

    if not isinstance(symptoms, str) or len(symptoms.strip()) == 0:
        return jsonify({"error": "Symptoms must be a non-empty string."}), 400

    # Call the Gemini model with the provided symptoms
    response_text = call_gemini(symptoms)

    return jsonify({"result": response_text})


# Run the app
if __name__ == '__main__':
    # Use 0.0.0.0 to make the app accessible on your local network
    app.run(host='0.0.0.0', port=5000, debug=True)
