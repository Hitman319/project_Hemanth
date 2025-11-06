"""
Test cases for AI-powered API routes
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_ai_hello_endpoint_without_api_key():
    """Test AI hello endpoint when API key is not configured"""
    with patch('app.core.config.settings.openai_api_key', None):
        response = client.get("/api/v1/ai-hello/John")
        assert response.status_code == 500
        error_detail = response.json()["detail"]
        assert ("OpenAI API key not configured" in error_detail or 
                "Error generating AI response" in error_detail)

@patch('app.api.routes.ai.ChatOpenAI')
def test_ai_hello_endpoint_success(mock_chat_openai):
    """Test AI hello endpoint with successful response"""
    # Mock the LLM response
    mock_llm = AsyncMock()
    mock_response = AsyncMock()
    mock_response.content = "Hello John! It's wonderful to meet you. Hope you're having a fantastic day!"
    mock_llm.ainvoke.return_value = mock_response
    mock_chat_openai.return_value = mock_llm
    
    response = client.get("/api/v1/ai-hello/John")
    assert response.status_code == 200
    assert "message" in response.json()
    # Note: In real testing, you might want to mock the actual API key check

@patch('app.api.routes.ai.ChatOpenAI')
def test_chat_endpoint_success(mock_chat_openai):
    """Test chat endpoint with successful response"""
    # Mock the LLM response
    mock_llm = AsyncMock()
    mock_response = AsyncMock()
    mock_response.content = "Hello! How can I help you today?"
    mock_llm.ainvoke.return_value = mock_response
    mock_chat_openai.return_value = mock_llm
    
    chat_request = {
        "message": "Hello, how are you?",
        "temperature": 0.7
    }
    
    response = client.post("/api/v1/chat", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert "model" in response_data
    assert response_data["model"] == "gpt-3.5-turbo"

def test_chat_endpoint_without_api_key():
    """Test chat endpoint when API key is not configured"""
    with patch('app.core.config.settings.openai_api_key', None):
        chat_request = {
            "message": "Hello, how are you?",
            "temperature": 0.7
        }
        response = client.post("/api/v1/chat", json=chat_request)
        assert response.status_code == 500
        error_detail = response.json()["detail"]
        assert ("OpenAI API key not configured" in error_detail or 
                "Error communicating with AI" in error_detail)

def test_chat_endpoint_invalid_request():
    """Test chat endpoint with invalid request data"""
    invalid_request = {
        "temperature": 0.7
        # Missing required 'message' field
    }
    
    response = client.post("/api/v1/chat", json=invalid_request)
    assert response.status_code == 422  # Validation error
