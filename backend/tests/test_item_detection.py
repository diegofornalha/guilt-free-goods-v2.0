"""
Test suite for item detection endpoints and functionality.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
from pathlib import Path

client = TestClient(app)

# Test data setup
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_IMAGE_PATH = TEST_DATA_DIR / "test_item.jpg"

@pytest.fixture(scope="module")
def test_image():
    """Create a test image for testing."""
    if not TEST_DATA_DIR.exists():
        TEST_DATA_DIR.mkdir(parents=True)
    
    # Create a simple test image if it doesn't exist
    if not TEST_IMAGE_PATH.exists():
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='white')
        img.save(TEST_IMAGE_PATH)
    
    return TEST_IMAGE_PATH

def test_analyze_item(test_image):
    """Test the analyze item endpoint."""
    with open(test_image, "rb") as f:
        files = {"image": ("test_item.jpg", f, "image/jpeg")}
        response = client.post("/api/item-detection/analyze", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    
    # Verify all required analysis components are present
    result = data["data"]
    assert "brand" in result
    assert "condition" in result
    assert "size" in result

def test_optimize_image(test_image):
    """Test the image optimization endpoint."""
    with open(test_image, "rb") as f:
        files = {"image": ("test_item.jpg", f, "image/jpeg")}
        response = client.post("/api/item-detection/optimize", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "optimized_image" in data["data"]
    assert "optimization_details" in data["data"]

def test_remove_background(test_image):
    """Test the background removal endpoint."""
    with open(test_image, "rb") as f:
        files = {"image": ("test_item.jpg", f, "image/jpeg")}
        response = client.post("/api/item-detection/remove-background", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "processed_image" in data["data"]
    assert "processing_details" in data["data"]

def test_detect_brand(test_image):
    """Test the brand detection endpoint."""
    with open(test_image, "rb") as f:
        files = {"image": ("test_item.jpg", f, "image/jpeg")}
        response = client.post("/api/item-detection/detect-brand", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "detected_brands" in data["data"]

def test_assess_condition(test_image):
    """Test the condition assessment endpoint."""
    with open(test_image, "rb") as f:
        files = {"image": ("test_item.jpg", f, "image/jpeg")}
        response = client.post("/api/item-detection/assess-condition", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "condition_grade" in data["data"]
    assert "wear_level" in data["data"]
    assert "condition_details" in data["data"]

def test_detect_size(test_image):
    """Test the size detection endpoint."""
    with open(test_image, "rb") as f:
        files = {"image": ("test_item.jpg", f, "image/jpeg")}
        response = client.post("/api/item-detection/detect-size", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "dimensions" in data["data"]
    assert "confidence" in data["data"]

def test_error_handling():
    """Test error handling for invalid requests."""
    # Test with invalid file
    files = {"image": ("test.txt", b"invalid data", "text/plain")}
    response = client.post("/api/item-detection/analyze", files=files)
    assert response.status_code == 500
    
    # Test with missing file
    response = client.post("/api/item-detection/analyze")
    assert response.status_code == 422  # FastAPI validation error
