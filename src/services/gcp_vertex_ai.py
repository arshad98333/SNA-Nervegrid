# src/services/gcp_vertex_ai.py

import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth
import google.auth.transport.requests

# Load environment variables from .env for local development
load_dotenv()

# --- Vertex AI Initialization ---
try:
    # Attempt to get credentials automatically (works for Cloud Run or local gcloud)
    creds, default_project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)

    # Use environment variables if provided
    project_id = os.getenv("GCP_PROJECT_ID") or default_project
    region = os.getenv("GCP_REGION")

    if not project_id or not region:
        raise ValueError("GCP_PROJECT_ID and GCP_REGION must be set either in .env or via environment.")

    # Initialize Vertex AI client
    vertexai.init(project=project_id, location=region, credentials=creds)

    # Initialize the model
    model = GenerativeModel("gemini-2.0-flash-lite-001")
    print(f"[INFO] Vertex AI initialized successfully for project '{project_id}' in region '{region}'.")

except Exception as e:
    print(f"[ERROR] Failed to initialize Vertex AI: {e}")
    model = None

# --- Core Function to Generate Text ---
def generate_text(prompt: str) -> str:
    """
    Generate text from a prompt using Vertex AI Gemini model.

    Args:
        prompt (str): The input prompt for the model.

    Returns:
        str: Generated text or an error message if initialization failed.
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
