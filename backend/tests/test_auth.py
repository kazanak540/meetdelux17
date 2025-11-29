import pytest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/app/backend')
from server import app

client = TestClient(app)

def test_register_user():
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "email": f"test_{pytest.__version__}@test.com",
        "password": "Test123!",
        "full_name": "Test User",
        "phone": "+905551234567",
        "role": "customer"
    })
    assert response.status_code in [200, 400]  # 400 if user exists

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "invalid@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 401
