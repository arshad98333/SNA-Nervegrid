import os
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

load_dotenv()

def process_document(file_content: bytes, mime_type: str) -> str:
    """
    Processes a document using Google Cloud Document AI to extract its text.

    Args:
        file_content (bytes): The raw byte content of the file.
        mime_type (str): The MIME type of the file (e.g., 'application/pdf').

    Returns:
        str: The extracted text content or a formatted error message.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    location = "us"  # Document AI processors are typically in 'us' or 'eu'
    processor_id = os.getenv("DOCAI_PROCESSOR_ID")
    
    if not all([project_id, location, processor_id]):
        return "Error: Document AI configuration (GCP_PROJECT_ID, DOCAI_PROCESSOR_ID) is missing in .env file."

    try:
        opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
        client = documentai.DocumentProcessorServiceClient(client_options=opts)
        name = client.processor_path(project_id, location, processor_id)

        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)

        result = client.process_document(request=request)
        print("[INFO] Document AI processing successful.")
        return result.document.text
    except Exception as e:
        error_message = f"Error calling Document AI. Check API is enabled, processor ID '{processor_id}' is correct and in region '{location}'. Details: {e}"
        print(f"[ERROR] {error_message}")
        return error_message