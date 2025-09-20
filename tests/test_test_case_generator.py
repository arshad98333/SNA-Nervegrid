"""
Comprehensive automated tests for the test case generator functionality.
"""

import pytest
import pandas as pd
import json
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.test_case_generator import generate_test_cases_from_doc
from utils.error_handler import ErrorHandler, validate_file_upload, handle_llm_response_error

class TestTestCaseGenerator:
    """Test cases for test case generator functionality."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Mock environment variables
        os.environ['GCP_PROJECT_ID'] = 'test-project'
        os.environ['GCP_REGION'] = 'us-central1'
        os.environ['DOCAI_PROCESSOR_ID'] = 'test-processor'
    
    def test_generate_test_cases_success(self):
        """Test successful test case generation."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        # Mock the GCP services
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = json.dumps([
                {
                    "id": "TC001",
                    "requirement_id": "REQ001",
                    "type": "positive",
                    "description": "Test user login with valid credentials",
                    "steps": "1. Navigate to login page\n2. Enter valid username\n3. Enter valid password\n4. Click login",
                    "expected_result": "User should be logged in successfully"
                }
            ])
            
            result = generate_test_cases_from_doc(file_content, mime_type)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert result.iloc[0]['id'] == "TC001"
            assert result.iloc[0]['type'] == "positive"
    
    def test_generate_test_cases_doc_ai_error(self):
        """Test handling of Document AI errors."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai:
            mock_doc_ai.return_value = "Error: Document AI processing failed"
            
            with pytest.raises(ValueError) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "Error:" in str(exc_info.value)
            assert "Document AI processing failed" in str(exc_info.value)
    
    def test_generate_test_cases_invalid_json(self):
        """Test handling of invalid JSON response from AI."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = "Invalid JSON response"
            
            with pytest.raises(ValueError) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "AI response was not valid JSON" in str(exc_info.value)
    
    def test_generate_test_cases_malformed_json(self):
        """Test handling of malformed JSON response."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = '{"incomplete": "json"'
            
            with pytest.raises(ValueError) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "AI response was not valid JSON" in str(exc_info.value)
    
    def test_generate_test_cases_empty_response(self):
        """Test handling of empty response from AI."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = ""
            
            with pytest.raises(ValueError) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "AI response was not valid JSON" in str(exc_info.value)
    
    def test_generate_test_cases_multiple_test_cases(self):
        """Test generation of multiple test cases."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        test_cases = [
            {
                "id": "TC001",
                "requirement_id": "REQ001",
                "type": "positive",
                "description": "Test user login with valid credentials",
                "steps": "1. Navigate to login page\n2. Enter valid username\n3. Enter valid password\n4. Click login",
                "expected_result": "User should be logged in successfully"
            },
            {
                "id": "TC002",
                "requirement_id": "REQ001",
                "type": "negative",
                "description": "Test user login with invalid credentials",
                "steps": "1. Navigate to login page\n2. Enter invalid username\n3. Enter invalid password\n4. Click login",
                "expected_result": "User should see error message"
            }
        ]
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = json.dumps(test_cases)
            
            result = generate_test_cases_from_doc(file_content, mime_type)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            assert result.iloc[0]['id'] == "TC001"
            assert result.iloc[1]['id'] == "TC002"
            assert result.iloc[0]['type'] == "positive"
            assert result.iloc[1]['type'] == "negative"
    
    def test_generate_test_cases_missing_required_fields(self):
        """Test handling of missing required fields in JSON response."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        incomplete_test_case = {
            "id": "TC001",
            "description": "Test case without required fields"
            # Missing: requirement_id, type, steps, expected_result
        }
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = json.dumps([incomplete_test_case])
            
            result = generate_test_cases_from_doc(file_content, mime_type)
            
            # Should still create DataFrame but with NaN values for missing fields
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert pd.isna(result.iloc[0]['requirement_id'])
            assert pd.isna(result.iloc[0]['type'])
    
    def test_generate_test_cases_vertex_ai_error(self):
        """Test handling of Vertex AI errors."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.side_effect = Exception("Vertex AI service unavailable")
            
            with pytest.raises(Exception) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "Vertex AI service unavailable" in str(exc_info.value)
    
    def test_generate_test_cases_with_markdown_code_blocks(self):
        """Test handling of JSON wrapped in markdown code blocks."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        test_cases = [
            {
                "id": "TC001",
                "requirement_id": "REQ001",
                "type": "positive",
                "description": "Test user login",
                "steps": "1. Navigate to login\n2. Enter credentials\n3. Click login",
                "expected_result": "User logged in successfully"
            }
        ]
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = f"```json\n{json.dumps(test_cases)}\n```"
            
            result = generate_test_cases_from_doc(file_content, mime_type)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert result.iloc[0]['id'] == "TC001"

class TestTestCaseGeneratorEdgeCases:
    """Test cases for edge cases in test case generation."""
    
    def test_generate_test_cases_very_large_document(self):
        """Test handling of very large documents."""
        file_content = b"Test requirements document" * 1000  # Large content
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text" * 1000
            mock_vertex_ai.return_value = json.dumps([{
                "id": "TC001",
                "requirement_id": "REQ001",
                "type": "positive",
                "description": "Test case for large document",
                "steps": "1. Test step",
                "expected_result": "Expected result"
            }])
            
            result = generate_test_cases_from_doc(file_content, mime_type)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
    
    def test_generate_test_cases_special_characters(self):
        """Test handling of special characters in test cases."""
        file_content = b"Test requirements document"
        mime_type = "application/pdf"
        
        test_cases = [
            {
                "id": "TC001",
                "requirement_id": "REQ001",
                "type": "positive",
                "description": "Test with special chars: @#$%^&*()",
                "steps": "1. Test step with émojis 🚀\n2. Another step with unicode: 中文",
                "expected_result": "Expected result with special chars: <>&\"'"
            }
        ]
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted requirements text"
            mock_vertex_ai.return_value = json.dumps(test_cases)
            
            result = generate_test_cases_from_doc(file_content, mime_type)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert "émojis" in result.iloc[0]['steps']
            assert "中文" in result.iloc[0]['steps']
    
    def test_generate_test_cases_empty_requirements(self):
        """Test handling of empty requirements document."""
        file_content = b""
        mime_type = "application/pdf"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai:
            mock_doc_ai.return_value = "Error: Empty document"
            
            with pytest.raises(ValueError) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "Error:" in str(exc_info.value)
    
    def test_generate_test_cases_unsupported_file_type(self):
        """Test handling of unsupported file types."""
        file_content = b"Test content"
        mime_type = "image/jpeg"  # Unsupported type
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai:
            mock_doc_ai.return_value = "Error: Unsupported file type"
            
            with pytest.raises(ValueError) as exc_info:
                generate_test_cases_from_doc(file_content, mime_type)
            
            assert "Error:" in str(exc_info.value)

if __name__ == "__main__":
    pytest.main([__file__])
