import os
from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()

# --- Initialization ---
try:
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set to initialize Firestore.")
    
    db = firestore.Client(project=project_id)
    print("[INFO] Firestore client initialized successfully.")
except Exception as e:
    print(f"[ERROR] Failed to initialize Firestore: {e}")
    db = None

# --- Core Functions ---
def save_record(collection_name: str, data: dict) -> tuple[bool, str]:
    """
    Saves a dictionary as a new document in a specified Firestore collection.

    Args:
        collection_name (str): The name of the collection (e.g., 'scan_history').
        data (dict): The data to save. A 'createdAt' timestamp will be added.

    Returns:
        tuple[bool, str]: (Success_flag, Document_ID or error_message).
    """
    if not db:
        return False, "Error: Firestore client is not initialized."
        
    try:
        data['createdAt'] = firestore.SERVER_TIMESTAMP
        doc_ref = db.collection(collection_name).add(data)[1]
        print(f"[INFO] Record saved to '{collection_name}' with ID: {doc_ref.id}")
        return True, doc_ref.id
    except Exception as e:
        print(f"[ERROR] Failed to save record to Firestore: {e}")
        return False, str(e)