"""
Comprehensive error handling and edge case management for the AI Compliance Co-Pilot.
"""

import streamlit as st
import logging
from typing import Any, Dict, Optional, Tuple
from functools import wraps
import traceback
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling and edge case management."""
    
    @staticmethod
    def handle_file_upload_error(error: Exception, file_type: str) -> str:
        """Handle file upload errors with specific guidance."""
        error_messages = {
            "FileNotFoundError": f"File not found. Please ensure the {file_type} file exists and is accessible.",
            "PermissionError": f"Permission denied. Please check file permissions for the {file_type} file.",
            "IsADirectoryError": f"Expected a file but found a directory. Please select a valid {file_type} file.",
            "FileTooLargeError": f"File too large. Please upload a {file_type} file smaller than 10MB.",
            "UnsupportedFileTypeError": f"Unsupported file type. Please upload a valid {file_type} file.",
        }
        
        error_type = type(error).__name__
        return error_messages.get(error_type, f"File upload error: {str(error)}")
    
    @staticmethod
    def handle_api_error(error: Exception, service: str) -> str:
        """Handle API-related errors with specific guidance."""
        error_messages = {
            "ConnectionError": f"Unable to connect to {service}. Please check your internet connection and try again.",
            "TimeoutError": f"Request to {service} timed out. Please try again with a smaller file or check your connection.",
            "AuthenticationError": f"Authentication failed with {service}. Please check your credentials and try again.",
            "RateLimitError": f"Rate limit exceeded for {service}. Please wait a moment and try again.",
            "ServiceUnavailableError": f"{service} is temporarily unavailable. Please try again later.",
        }
        
        error_type = type(error).__name__
        return error_messages.get(error_type, f"API error with {service}: {str(error)}")
    
    @staticmethod
    def handle_validation_error(error: Exception, field: str) -> str:
        """Handle validation errors with specific guidance."""
        return f"Validation error in {field}: {str(error)}. Please check your input and try again."
    
    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """Log errors with context for debugging."""
        logger.error(f"Error in {context}: {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

def safe_execute(func):
    """Decorator for safe execution with error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.log_error(e, func.__name__)
            st.error(f"An error occurred in {func.__name__}: {str(e)}")
            return None
    return wrapper

def validate_environment() -> Tuple[bool, str]:
    """Validate that all required environment variables are set."""
    required_vars = ["GCP_PROJECT_ID", "GCP_REGION"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        return False, f"Missing required environment variables: {', '.join(missing_vars)}"
    
    return True, "Environment validation passed"

def validate_file_upload(file, allowed_types: list, max_size_mb: int = 10) -> Tuple[bool, str]:
    """Validate uploaded file for type and size."""
    if file is None:
        return False, "No file uploaded"
    
    # Check file type
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in allowed_types:
        return False, f"Unsupported file type. Allowed types: {', '.join(allowed_types)}"
    
    # Check file size
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File too large. Maximum size: {max_size_mb}MB"
    
    return True, "File validation passed"

def handle_llm_response_error(response: str) -> Tuple[bool, str]:
    """Validate and handle LLM response errors."""
    if not response or response.strip() == "":
        return False, "Empty response from AI service"
    
    if "Error:" in response or "error:" in response.lower():
        return False, f"AI service returned an error: {response}"
    
    if len(response) < 10:
        return False, "Response too short, may be incomplete"
    
    return True, "Response validation passed"

def create_error_ui(error_type: str, error_message: str, suggestions: list = None) -> None:
    """Create a professional error UI with suggestions."""
    st.error(f"""
    **{error_type}**
    
    {error_message}
    """)
    
    if suggestions:
        with st.expander("💡 Troubleshooting Suggestions", expanded=True):
            for i, suggestion in enumerate(suggestions, 1):
                st.write(f"{i}. {suggestion}")

def handle_edge_cases():
    """Handle common edge cases and provide user guidance."""
    
    # Check for very small screens
    if st.session_state.get('screen_width', 1200) < 768:
        st.warning("""
        **Mobile Device Detected**
        
        For the best experience, please use a desktop or tablet device. 
        Some features may not be fully functional on mobile devices.
        """)
    
    # Check for slow connection
    if st.session_state.get('connection_slow', False):
        st.info("""
        **Slow Connection Detected**
        
        Large file uploads may take longer than usual. Please be patient.
        """)
    
    # Check for browser compatibility
    if st.session_state.get('browser_old', False):
        st.warning("""
        **Browser Compatibility Warning**
        
        For the best experience, please use a modern browser (Chrome, Firefox, Safari, Edge).
        """)

def create_loading_state(message: str = "Processing...") -> None:
    """Create a professional loading state."""
    with st.spinner(message):
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 12px;
            margin: 1rem 0;
        ">
            <div style="font-size: 1.125rem; color: #1e40af; margin-bottom: 0.5rem;">
                {message}
            </div>
            <div style="font-size: 0.875rem; color: #64748b;">
                This may take a few moments...
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_success_state(message: str = "Operation completed successfully!") -> None:
    """Create a professional success state."""
    st.success(f"""
    **Success!**
    
    {message}
    """)

def create_warning_state(message: str, details: str = None) -> None:
    """Create a professional warning state."""
    st.warning(f"""
    **Warning**
    
    {message}
    """)
    
    if details:
        st.info(f"**Details:** {details}")

# Edge case handlers for specific scenarios
class EdgeCaseHandlers:
    """Handlers for specific edge cases."""
    
    @staticmethod
    def handle_empty_document(content: str) -> bool:
        """Handle empty or invalid document content."""
        if not content or len(content.strip()) < 50:
            st.warning("""
            **Document Content Issue**
            
            The uploaded document appears to be empty or too short for analysis.
            Please ensure the document contains sufficient text content.
            """)
            return False
        return True
    
    @staticmethod
    def handle_unsupported_language(content: str) -> bool:
        """Handle documents in unsupported languages."""
        # Simple check for non-English content
        non_ascii_ratio = sum(1 for char in content if ord(char) > 127) / len(content)
        if non_ascii_ratio > 0.3:
            st.warning("""
            **Language Support Warning**
            
            The document appears to contain non-English content. 
            For best results, please use English documents or ensure the content is primarily in English.
            """)
        return True
    
    @staticmethod
    def handle_large_document(content: str, max_chars: int = 50000) -> bool:
        """Handle very large documents."""
        if len(content) > max_chars:
            st.warning(f"""
            **Large Document Warning**
            
            The document is very large ({len(content):,} characters). 
            Processing may take longer than usual, and some content may be truncated.
            """)
        return True
    
    @staticmethod
    def handle_sensitive_content(content: str) -> bool:
        """Handle potentially sensitive content."""
        sensitive_keywords = ['password', 'ssn', 'credit card', 'bank account', 'social security']
        content_lower = content.lower()
        
        for keyword in sensitive_keywords:
            if keyword in content_lower:
                st.warning("""
                **Sensitive Content Detected**
                
                The document may contain sensitive information. 
                Please ensure you have the right to process this content.
                """)
                break
        return True
