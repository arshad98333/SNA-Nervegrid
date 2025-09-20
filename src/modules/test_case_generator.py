import pandas as pd
import json
from src.services import gcp_doc_ai, gcp_vertex_ai

def generate_test_cases_from_doc(file_content: bytes, mime_type: str) -> pd.DataFrame:
    extracted_text = gcp_doc_ai.process_document(file_content, mime_type)
    if "Error:" in extracted_text:
        raise ValueError(extracted_text)

    prompt = f"""
    You are an expert AI Test Case Generator for enterprise software. Your task is to analyze the following requirements document and generate a comprehensive, structured test suite in JSON format.

    Instructions:
    1. Create test cases covering positive, negative, edge, and compliance scenarios.
    2. Ensure every test case is directly traceable to a requirement ID from the document.
    3. The output must be a single, valid JSON array of objects, with no additional text or explanations.
    4. Each object must contain these exact keys: "id", "requirement_id", "type", "description", "steps", "expected_result".

    Document for Analysis:
    ---
    {extracted_text}
    ---
    """
    response_text = gcp_vertex_ai.generate_text(prompt)
    cleaned_response = response_text.strip().replace("```json", "").replace("```", "")
    
    try:
        return pd.DataFrame(json.loads(cleaned_response))
    except json.JSONDecodeError as e:
        raise ValueError(f"AI response was not valid JSON. Error: {e}. Response: {cleaned_response}")