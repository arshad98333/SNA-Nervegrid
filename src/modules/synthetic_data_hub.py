from src.services import gcp_vertex_ai
import json
import pandas as pd

def generate_synthetic_data(prompt: str) -> tuple[str, pd.DataFrame]:
    full_prompt = f"""
    You are a synthetic data generator. Based on the user's request, create realistic but fake data.
    The output must be a single, valid JSON array of objects, with no explanations.
    
    User Request: "{prompt}"
    """
    response_text = gcp_vertex_ai.generate_text(full_prompt)
    cleaned_response = response_text.strip().replace("```json", "").replace("```", "")

    try:
        df = pd.read_json(cleaned_response)
        return cleaned_response, df
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"AI response could not be parsed into a DataFrame. Error: {e}")