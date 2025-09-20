import os
from dotenv import load_dotenv
from google.cloud import dlp_v2

load_dotenv()

def inspect_text(text_to_scan: str) -> list[dict]:
    """
    Scans a block of text for sensitive data using the Cloud DLP API.

    Args:
        text_to_scan (str): The text to be inspected.

    Returns:
        list[dict]: A list of findings. Returns an empty list on error.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("[ERROR] GCP_PROJECT_ID not set for DLP inspection.")
        return []

    try:
        dlp_client = dlp_v2.DlpServiceClient()
        parent = f"projects/{project_id}"
        item = {"value": text_to_scan}

        info_types = [
            {"name": "AADHAAR_NUMBER"}, {"name": "INDIA_PAN_INDIVIDUAL"},
            {"name": "PHONE_NUMBER"}, {"name": "EMAIL_ADDRESS"}
        ]

        request = {
            "parent": parent,
            "inspect_config": {"info_types": info_types, "include_quote": True},
            "item": item,
        }

        response = dlp_client.inspect_content(request=request)
        
        findings = [{
            "quote": finding.quote,
            "info_type": finding.info_type.name,
            "likelihood": str(finding.likelihood).split('.')[-1]
        } for finding in response.result.findings]
        
        print(f"[INFO] DLP scan complete. Found {len(findings)} potential PII items.")
        return findings
    except Exception as e:
        print(f"[ERROR] Could not perform DLP inspection: {e}")
        return []