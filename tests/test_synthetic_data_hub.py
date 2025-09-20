"""
Comprehensive automated tests for the synthetic data hub functionality.
"""

import pytest
import pandas as pd
import json
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.synthetic_data_hub import generate_synthetic_data
from utils.error_handler import ErrorHandler, handle_llm_response_error

class TestSyntheticDataHub:
    """Test cases for synthetic data hub functionality."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Mock environment variables
        os.environ['GCP_PROJECT_ID'] = 'test-project'
        os.environ['GCP_REGION'] = 'us-central1'
    
    def test_generate_synthetic_data_success(self):
        """Test successful synthetic data generation."""
        prompt = "Generate 5 patient records with name, age, and diagnosis"
        
        # Mock the GCP service
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps([
                {
                    "name": "John Doe",
                    "age": 35,
                    "diagnosis": "Hypertension"
                },
                {
                    "name": "Jane Smith",
                    "age": 28,
                    "diagnosis": "Diabetes"
                }
            ])
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(json_str, str)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert "name" in df.columns
            assert "age" in df.columns
            assert "diagnosis" in df.columns
    
    def test_generate_synthetic_data_invalid_json(self):
        """Test handling of invalid JSON response from AI."""
        prompt = "Generate patient records"
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = "Invalid JSON response"
            
            with pytest.raises(ValueError) as exc_info:
                generate_synthetic_data(prompt)
            
            assert "AI response could not be parsed into a DataFrame" in str(exc_info.value)
    
    def test_generate_synthetic_data_malformed_json(self):
        """Test handling of malformed JSON response."""
        prompt = "Generate patient records"
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = '{"incomplete": "json"'
            
            with pytest.raises(ValueError) as exc_info:
                generate_synthetic_data(prompt)
            
            assert "AI response could not be parsed into a DataFrame" in str(exc_info.value)
    
    def test_generate_synthetic_data_empty_response(self):
        """Test handling of empty response from AI."""
        prompt = "Generate patient records"
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = ""
            
            with pytest.raises(ValueError) as exc_info:
                generate_synthetic_data(prompt)
            
            assert "AI response could not be parsed into a DataFrame" in str(exc_info.value)
    
    def test_generate_synthetic_data_vertex_ai_error(self):
        """Test handling of Vertex AI errors."""
        prompt = "Generate patient records"
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.side_effect = Exception("Vertex AI service unavailable")
            
            with pytest.raises(Exception) as exc_info:
                generate_synthetic_data(prompt)
            
            assert "Vertex AI service unavailable" in str(exc_info.value)
    
    def test_generate_synthetic_data_with_markdown_code_blocks(self):
        """Test handling of JSON wrapped in markdown code blocks."""
        prompt = "Generate patient records"
        
        data = [
            {
                "name": "John Doe",
                "age": 35,
                "diagnosis": "Hypertension"
            }
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = f"```json\n{json.dumps(data)}\n```"
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(json_str, str)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
    
    def test_generate_synthetic_data_large_dataset(self):
        """Test generation of large datasets."""
        prompt = "Generate 1000 patient records"
        
        # Create large dataset
        large_data = []
        for i in range(1000):
            large_data.append({
                "id": i,
                "name": f"Patient {i}",
                "age": 20 + (i % 60),
                "diagnosis": f"Condition {i % 10}"
            })
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(large_data)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1000
            assert "id" in df.columns
            assert "name" in df.columns
    
    def test_generate_synthetic_data_complex_schema(self):
        """Test generation of data with complex schema."""
        prompt = "Generate medical records with complex schema"
        
        complex_data = [
            {
                "patient_id": "P001",
                "personal_info": {
                    "name": "John Doe",
                    "age": 35,
                    "gender": "Male"
                },
                "medical_history": [
                    {"condition": "Hypertension", "year": 2020},
                    {"condition": "Diabetes", "year": 2021}
                ],
                "current_medications": [
                    {"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"}
                ],
                "last_visit": "2024-01-15",
                "next_appointment": "2024-02-15"
            }
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(complex_data)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
            assert "patient_id" in df.columns
            assert "personal_info" in df.columns

class TestSyntheticDataHubEdgeCases:
    """Test cases for edge cases in synthetic data generation."""
    
    def test_generate_synthetic_data_special_characters(self):
        """Test handling of special characters in data."""
        prompt = "Generate data with special characters"
        
        data_with_special_chars = [
            {
                "name": "José María",
                "description": "Patient with émojis 🏥 and unicode: 中文",
                "notes": "Special chars: @#$%^&*()",
                "html_content": "<div>HTML content</div>"
            }
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(data_with_special_chars)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
            assert "José María" in df.iloc[0]['name']
            assert "émojis" in df.iloc[0]['description']
    
    def test_generate_synthetic_data_empty_prompt(self):
        """Test handling of empty prompt."""
        prompt = ""
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps([{"id": 1, "value": "test"}])
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
    
    def test_generate_synthetic_data_very_long_prompt(self):
        """Test handling of very long prompts."""
        prompt = "Generate data " * 1000  # Very long prompt
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps([{"id": 1, "value": "test"}])
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
    
    def test_generate_synthetic_data_numeric_data(self):
        """Test generation of numeric data."""
        prompt = "Generate numeric data"
        
        numeric_data = [
            {"value": 42, "float_value": 3.14159, "negative": -10},
            {"value": 100, "float_value": 2.71828, "negative": -5.5}
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(numeric_data)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert df['value'].dtype in ['int64', 'float64']
            assert df['float_value'].dtype == 'float64'
    
    def test_generate_synthetic_data_boolean_data(self):
        """Test generation of boolean data."""
        prompt = "Generate boolean data"
        
        boolean_data = [
            {"active": True, "verified": False, "enabled": True},
            {"active": False, "verified": True, "enabled": False}
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(boolean_data)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert df['active'].dtype == 'bool'
            assert df['verified'].dtype == 'bool'
    
    def test_generate_synthetic_data_null_values(self):
        """Test handling of null values in data."""
        prompt = "Generate data with null values"
        
        data_with_nulls = [
            {"name": "John", "age": 35, "middle_name": None},
            {"name": "Jane", "age": None, "middle_name": "Marie"},
            {"name": None, "age": 28, "middle_name": "Ann"}
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(data_with_nulls)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 3
            assert pd.isna(df.iloc[0]['middle_name'])
            assert pd.isna(df.iloc[1]['age'])
            assert pd.isna(df.iloc[2]['name'])
    
    def test_generate_synthetic_data_nested_objects(self):
        """Test handling of nested objects in data."""
        prompt = "Generate data with nested objects"
        
        nested_data = [
            {
                "user": {
                    "id": 1,
                    "profile": {
                        "name": "John",
                        "settings": {
                            "theme": "dark",
                            "notifications": True
                        }
                    }
                },
                "metadata": {
                    "created_at": "2024-01-01",
                    "tags": ["user", "active"]
                }
            }
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(nested_data)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
            assert "user" in df.columns
            assert "metadata" in df.columns
    
    def test_generate_synthetic_data_array_data(self):
        """Test handling of array data."""
        prompt = "Generate data with arrays"
        
        array_data = [
            {
                "id": 1,
                "tags": ["urgent", "medical", "review"],
                "scores": [85, 92, 78, 90],
                "coordinates": [40.7128, -74.0060]
            }
        ]
        
        with patch('src.services.gcp_vertex_ai.generate_text') as mock_vertex_ai:
            mock_vertex_ai.return_value = json.dumps(array_data)
            
            json_str, df = generate_synthetic_data(prompt)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
            assert "tags" in df.columns
            assert "scores" in df.columns
            assert "coordinates" in df.columns

if __name__ == "__main__":
    pytest.main([__file__])
