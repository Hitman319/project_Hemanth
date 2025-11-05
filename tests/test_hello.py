"""
Test cases for Hello World API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Hemanth's Hello World API"}


def test_hello_world():
    """Test the basic hello world endpoint"""
    response = client.get("/api/v1/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "HELLO WORLD"}


def test_hello_person():
    """Test the personalized hello endpoint"""
    response = client.get("/api/v1/hello/John")
    assert response.status_code == 200
    assert response.json() == {"message": "HELLO JOHN"}


def test_hello_world_post():
    """Test the hello world POST endpoint"""
    response = client.post("/api/v1/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "HELLO WORLD"}


def test_hello_person_lowercase():
    """Test personalized hello with lowercase name"""
    response = client.get("/api/v1/hello/hemanth")
    assert response.status_code == 200
    assert response.json() == {"message": "HELLO HEMANTH"}


def test_hello_person_mixed_case():
    """Test personalized hello with mixed case name"""
    response = client.get("/api/v1/hello/HeMaNtH")
    assert response.status_code == 200
    assert response.json() == {"message": "HELLO HEMANTH"}
