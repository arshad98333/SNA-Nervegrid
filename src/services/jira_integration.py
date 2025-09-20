from jira import JIRA
import pandas as pd

def export_test_cases_to_jira(
    df: pd.DataFrame, 
    server_url: str, 
    email: str, 
    api_token: str, 
    project_key: str, 
    issue_type: str = "Test"
) -> tuple[bool, str]:
    """
    Exports a DataFrame of test cases to a Jira project.

    Returns:
        A tuple (success_boolean, message_string).
    """
    try:
        jira_client = JIRA(server=server_url, basic_auth=(email, api_token))
        
        # Verify project exists
        jira_client.project(project_key)

        created_count = 0
        for index, row in df.iterrows():
            summary = f"TC: {row.get('description', 'Untitled Test Case')}"
            description = (
                f"h2. Test Case Details\n\n"
                f"*Requirement ID:* {row.get('requirement_id', 'N/A')}\n"
                f"*Test Type:* {row.get('type', 'N/A')}\n\n"
                f"h3. Steps to Reproduce\n{row.get('steps', 'No steps provided.')}\n\n"
                f"h3. Expected Result\n{row.get('expected_result', 'No expected result provided.')}"
            )
            
            issue_dict = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
            }
            
            jira_client.create_issue(fields=issue_dict)
            created_count += 1
        
        return True, f"Successfully created {created_count} test case issues in Jira project '{project_key}'."

    except Exception as e:
        # Provide a more helpful error message
        error_msg = str(e)
        if "401" in error_msg:
            message = "Authentication failed. Please check your Jira URL, email, and API token."
        elif "404" in error_msg:
            message = f"Could not find Jira project with key '{project_key}'. Please check the Project Key."
        else:
            message = f"An unexpected error occurred: {error_msg}"
        return False, message