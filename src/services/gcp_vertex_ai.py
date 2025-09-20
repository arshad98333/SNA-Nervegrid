import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

load_dotenv()

# --- Initialization ---
try:
    project_id = os.getenv("GCP_PROJECT_ID")
    region = os.getenv("GCP_REGION")
    
    if not all([project_id, region]):
        raise ValueError("GCP_PROJECT_ID and GCP_REGION must be set in the .env file.")
        
    vertexai.init(project=project_id, location=region)
    model = GenerativeModel("gemini-2.0-flash-lite-001")
    print("[INFO] Vertex AI client initialized successfully with Gemini 1.5 Pro.")
except Exception as e:
    print(f"[ERROR] Failed to initialize Vertex AI: {e}")
    model = None

# --- Core Functions ---
def generate_text(prompt: str) -> str:
    """
    Invokes the Gemini 1.5 Pro model to generate text from a prompt.

    Args:
        prompt (str): The text prompt to send to the model.

    Returns:
        str: The generated text response or a formatted error message.
    """
    if not model:
        return "Error: Vertex AI client is not initialized. Check server logs."
        
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_message = f"Error: Could not generate response from Vertex AI. Details: {e}"
        print(f"[ERROR] {error_message}")
        return error_message