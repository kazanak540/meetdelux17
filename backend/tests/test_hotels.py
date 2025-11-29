import pytest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/app/backend')
from server import app

client = TestClient(app)

def test_get_hotels():
    """Test getting hotel list"""
    response = client.get("/api/hotels")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_hotel_by_id():
    """Test getting specific hotel"""
    # First get a hotel ID
    hotels_response = client.get("/api/hotels?limit=1")
    if hotels_response.status_code == 200 and hotels_response.json():
        hotel_id = hotels_response.json()[0]['id']
        response = client.get(f"/api/hotels/{hotel_id}")
        assert response.status_code == 200
        assert response.json()['id'] == hotel_id

def test_get_rooms():
    """Test getting conference rooms"""
    response = client.get("/api/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
