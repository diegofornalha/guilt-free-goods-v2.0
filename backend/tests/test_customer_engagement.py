import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db

client = TestClient(app)

def test_create_message():
    """Test message creation endpoint with automated response."""
    payload = {
        "conversation_id": 1,
        "sender": "user",
        "content": "Hello, I have a question about an item"
    }
    
    response = client.post("/api/customer/message", json=payload)
    assert response.status_code == 200
    
    # Verify response structure
    data = response.json()
    assert "user_message" in data
    assert "auto_response" in data
    
    # Verify user message
    user_msg = data["user_message"]
    assert user_msg["conversationId"] == payload["conversation_id"]
    assert user_msg["sender"] == payload["sender"]
    assert user_msg["content"] == payload["content"]
    
    # Verify automated response
    auto_msg = data["auto_response"]
    assert auto_msg["conversationId"] == payload["conversation_id"]
    assert auto_msg["sender"] == "system"
    assert "Thank you for your message" in auto_msg["content"]

def test_create_message_invalid_conversation():
    """Test message creation with non-existent conversation ID."""
    payload = {
        "conversation_id": 999999,  # Non-existent ID
        "sender": "user",
        "content": "Test message"
    }
    
    response = client.post("/api/customer/message", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"

def test_create_message_validation():
    """Test input validation for message creation."""
    # Missing required fields
    payload = {
        "sender": "user"  # Missing conversation_id and content
    }
    
    response = client.post("/api/customer/message", json=payload)
    assert response.status_code == 422  # Validation error
