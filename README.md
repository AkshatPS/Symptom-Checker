# AI Symptom Checker

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-Flask-black.svg)](https://flask.palletsprojects.com/)

An educational web application that takes user-described symptoms and leverages a Large Language Model (LLM) to suggest potential conditions and responsible next steps. This tool is designed for informational purposes only and is not a substitute for professional medical advice.

---

## ## Live Demo

You can access the live, deployed version of this application here:

**[https://symptom-checker-ai-g8ag.onrender.com/](https://symptom-checker-ai-g8ag.onrender.com/)**

---

## ## Demo Video

A brief video walkthrough demonstrating the application's features and functionality.

**[Link to Demo Video](YOUR-DEMO-VIDEO-URL)**

---

## ## Features

* **Symptom Analysis:** Users can describe their symptoms in a simple, natural language text area.
* **LLM-Powered Insights:** Utilizes the Google Gemini API to analyze the input and generate a list of possible conditions.
* **Actionable Recommendations:** Provides safe, general next steps, emphasizing consultation with a healthcare professional.
* **Built-in Safety:** The prompt and model are configured with strong disclaimers and safety settings to ensure responsible outputs.
* **Responsive Frontend:** A clean, modern, and responsive user interface built with HTML, CSS, and vanilla JavaScript.

---

## ## Tech Stack

* **Backend:** Python, Flask
* **LLM:** Google Gemini API
* **Production Server:** Gunicorn
* **Frontend:** HTML5, CSS3, JavaScript (ES6)
* **Deployment:** Render

---

## ## Local Setup and Installation

To run this project on your local machine, please follow these steps:

### ### Prerequisites

* Python 3.9+
* Git
* A Google Gemini API Key

### ### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR-GITHUB-USERNAME]/symptom-checker.git
    cd symptom-checker
    ```

2.  **Create and activate a virtual environment:**
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    * Create a file named `.env` in the root directory of the project.
    * Add your Google Gemini API key to this file:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

5.  **Run the Flask application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

---

## ## API Endpoint

The application exposes a single API endpoint for processing symptoms.

* **Endpoint:** `/check_symptoms`
* **Method:** `POST`
* **Request Body (JSON):**
    ```json
    {
      "symptoms": "I have a sore throat, headache, and a slight fever."
    }
    ```
* **Success Response (JSON):**
    ```json
    {
      "result": "..." // LLM-generated text response
    }
    ```

---

## ## Project Structure

```
.
├── static/
│   ├── styles.css
│   └── script.js
├── templates/
│   └── index.html
├── .env
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## ## Disclaimer

This tool is for **educational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition.

---

