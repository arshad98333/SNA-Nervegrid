from src.services import gcp_doc_ai, gcp_vertex_ai

def analyze_document_compliance(file_content: bytes, mime_type: str, standard_persona: str) -> str:
    extracted_text = gcp_doc_ai.process_document(file_content, mime_type)
    if "Error:" in extracted_text:
        return extracted_text

    prompt = f"""
    As an AI assistant role-playing as {standard_persona}, your task is to conduct a meticulous compliance audit of the provided software requirements document.

    Instructions:
    1. Analyze the text strictly from the perspective of your assigned role.
    2. Identify and list all potential violations, risks, or ambiguities related to the regulations you oversee.
    3. For each finding, provide a clear classification:
       - **[Risk - High]:** Direct violations of core regulatory principles.
       - **[Warning - Medium]:** Vague language, missing safeguards, or deviation from best practices.
       - **[Pass]:** Areas that demonstrate clear compliance.
    4. For each point, cite the specific requirement ID or section from the document if possible.
    5. Provide a concise, actionable recommendation for remediation for each risk and warning.
    6. Format your entire response in structured Markdown.

    Document for Analysis:
    ---
    {extracted_text}
    ---
    """
    
    return gcp_vertex_ai.generate_text(prompt)