"""
Comprehensive automated tests for the compliance scanner functionality.
"""

import pytest
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.compliance_scanner import analyze_document_compliance
from utils.error_handler import ErrorHandler, validate_file_upload, handle_llm_response_error

class TestComplianceScanner:
    """Test cases for compliance scanner functionality."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Mock environment variables
        os.environ['GCP_PROJECT_ID'] = 'test-project'
        os.environ['GCP_REGION'] = 'us-central1'
        os.environ['DOCAI_PROCESSOR_ID'] = 'test-processor'
    
    def test_analyze_document_compliance_success(self):
        """Test successful document compliance analysis."""
        # Mock file content and MIME type
        file_content = b"Test document content for compliance analysis"
        mime_type = "application/pdf"
        standard_persona = "An expert on DPDPA compliance"
        
        # Mock the GCP services
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted text from document"
            mock_vertex_ai.return_value = "[Risk - High] Test risk finding\nThis is a test risk finding."
            
            result = analyze_document_compliance(file_content, mime_type, standard_persona)
            
            assert result is not None
            assert "[Risk - High]" in result
            mock_doc_ai.assert_called_once_with(file_content, mime_type)
            mock_vertex_ai.assert_called_once()
    
    def test_analyze_document_compliance_doc_ai_error(self):
        """Test handling of Document AI errors."""
        file_content = b"Test document content"
        mime_type = "application/pdf"
        standard_persona = "An expert on DPDPA compliance"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai:
            mock_doc_ai.return_value = "Error: Document AI processing failed"
            
            result = analyze_document_compliance(file_content, mime_type, standard_persona)
            
            assert "Error:" in result
            assert "Document AI processing failed" in result
    
    def test_analyze_document_compliance_vertex_ai_error(self):
        """Test handling of Vertex AI errors."""
        file_content = b"Test document content"
        mime_type = "application/pdf"
        standard_persona = "An expert on DPDPA compliance"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai, \
             patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            
            mock_doc_ai.return_value = "Extracted text from document"
            mock_vertex_ai.return_value = "Error: Vertex AI service unavailable"
            
            result = analyze_document_compliance(file_content, mime_type, standard_persona)
            
            assert "Error:" in result
            assert "Vertex AI service unavailable" in result
    
    def test_analyze_document_compliance_empty_content(self):
        """Test handling of empty document content."""
        file_content = b""
        mime_type = "application/pdf"
        standard_persona = "An expert on DPDPA compliance"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai:
            mock_doc_ai.return_value = "Error: Empty document"
            
            result = analyze_document_compliance(file_content, mime_type, standard_persona)
            
            assert "Error:" in result
            assert "Empty document" in result
    
    def test_analyze_document_compliance_invalid_mime_type(self):
        """Test handling of invalid MIME types."""
        file_content = b"Test content"
        mime_type = "invalid/type"
        standard_persona = "An expert on DPDPA compliance"
        
        with patch('src.services.gcp_doc_ai.process_document') as mock_doc_ai:
            mock_doc_ai.return_value = "Error: Unsupported MIME type"
            
            result = analyze_document_compliance(file_content, mime_type, standard_persona)
            
            assert "Error:" in result
            assert "Unsupported MIME type" in result

class TestErrorHandler:
    """Test cases for error handling functionality."""
    
    def test_handle_file_upload_error(self):
        """Test file upload error handling."""
        error = FileNotFoundError("File not found")
        result = ErrorHandler.handle_file_upload_error(error, "PDF")
        
        assert "File not found" in result
        assert "PDF" in result
    
    def test_handle_api_error(self):
        """Test API error handling."""
        error = ConnectionError("Connection failed")
        result = ErrorHandler.handle_api_error(error, "Document AI")
        
        assert "Unable to connect" in result
        assert "Document AI" in result
    
    def test_handle_validation_error(self):
        """Test validation error handling."""
        error = ValueError("Invalid input")
        result = ErrorHandler.handle_validation_error(error, "email")
        
        assert "Validation error" in result
        assert "email" in result

class TestValidationFunctions:
    """Test cases for validation functions."""
    
    def test_validate_file_upload_success(self):
        """Test successful file upload validation."""
        mock_file = Mock()
        mock_file.name = "test.pdf"
        mock_file.size = 1024 * 1024  # 1MB
        
        is_valid, message = validate_file_upload(mock_file, ["pdf", "docx"], 10)
        
        assert is_valid
        assert "File validation passed" in message
    
    def test_validate_file_upload_no_file(self):
        """Test file upload validation with no file."""
        is_valid, message = validate_file_upload(None, ["pdf", "docx"], 10)
        
        assert not is_valid
        assert "No file uploaded" in message
    
    def test_validate_file_upload_wrong_type(self):
        """Test file upload validation with wrong file type."""
        mock_file = Mock()
        mock_file.name = "test.txt"
        mock_file.size = 1024 * 1024
        
        is_valid, message = validate_file_upload(mock_file, ["pdf", "docx"], 10)
        
        assert not is_valid
        assert "Unsupported file type" in message
    
    def test_validate_file_upload_too_large(self):
        """Test file upload validation with file too large."""
        mock_file = Mock()
        mock_file.name = "test.pdf"
        mock_file.size = 15 * 1024 * 1024  # 15MB
        
        is_valid, message = validate_file_upload(mock_file, ["pdf", "docx"], 10)
        
        assert not is_valid
        assert "File too large" in message
    
    def test_handle_llm_response_error_empty(self):
        """Test LLM response error handling with empty response."""
        is_valid, message = handle_llm_response_error("")
        
        assert not is_valid
        assert "Empty response" in message
    
    def test_handle_llm_response_error_contains_error(self):
        """Test LLM response error handling with error in response."""
        is_valid, message = handle_llm_response_error("Error: Something went wrong")
        
        assert not is_valid
        assert "AI service returned an error" in message
    
    def test_handle_llm_response_error_too_short(self):
        """Test LLM response error handling with response too short."""
        is_valid, message = handle_llm_response_error("OK")
        
        assert not is_valid
        assert "Response too short" in message
    
    def test_handle_llm_response_success(self):
        """Test successful LLM response handling."""
        is_valid, message = handle_llm_response_error("This is a valid response from the AI service.")
        
        assert is_valid
        assert "Response validation passed" in message

class TestEdgeCases:
    """Test cases for edge case handling."""
    
    def test_handle_empty_document(self):
        """Test handling of empty documents."""
        from utils.error_handler import EdgeCaseHandlers
        
        # Test with empty content
        result = EdgeCaseHandlers.handle_empty_document("")
        assert not result
        
        # Test with very short content
        result = EdgeCaseHandlers.handle_empty_document("Short")
        assert not result
        
        # Test with sufficient content
        result = EdgeCaseHandlers.handle_empty_document("This is a sufficiently long document content for testing purposes.")
        assert result
    
    def test_handle_unsupported_language(self):
        """Test handling of unsupported languages."""
        from utils.error_handler import EdgeCaseHandlers
        
        # Test with English content
        result = EdgeCaseHandlers.handle_unsupported_language("This is English content.")
        assert result
        
        # Test with mixed content
        result = EdgeCaseHandlers.handle_unsupported_language("This is English with some 中文 content.")
        assert result
    
    def test_handle_large_document(self):
        """Test handling of large documents."""
        from utils.error_handler import EdgeCaseHandlers
        
        # Test with normal content
        result = EdgeCaseHandlers.handle_large_document("Normal content")
        assert result
        
        # Test with large content
        large_content = "A" * 60000  # 60k characters
        result = EdgeCaseHandlers.handle_large_document(large_content)
        assert result
    
    def test_handle_sensitive_content(self):
        """Test handling of sensitive content."""
        from utils.error_handler import EdgeCaseHandlers
        
        # Test with normal content
        result = EdgeCaseHandlers.handle_sensitive_content("Normal document content")
        assert result
        
        # Test with sensitive content
        result = EdgeCaseHandlers.handle_sensitive_content("User password is 123456")
        assert result

if __name__ == "__main__":
    pytest.main([__file__])
