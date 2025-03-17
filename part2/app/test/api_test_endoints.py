import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

@pytest.fixture
def test_user():
    """Create a test user and return the user ID."""
    response = requests.post(f"{BASE_URL}/users/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com"
    })
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def test_place(test_user):
    """Create a test place and return the place ID."""
    response = requests.post(f"{BASE_URL}/places/", json={
        "title": "Test Place",
        "description": "A nice test place.",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": test_user,
        
        "amenities": []
    })
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def test_review(test_user, test_place):
    """Create a test review and return the review ID."""
    response = requests.post(f"{BASE_URL}/reviews/", json={
        "text": "Great place!",
        "rating": 5,
        "user_id": test_user,
        "place_id": test_place
    })
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def test_amenity():
    """Create a test amenity and return the amenity ID."""
    response = requests.post(f"{BASE_URL}/amenities/", json={
        "name": "WiFi"
    })
    assert response.status_code == 201
    return response.json()["id"]

# ----------------- USERS TESTS -----------------

def test_get_user(test_user):
    response = requests.get(f"{BASE_URL}/users/{test_user}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user

def test_list_users():
    response = requests.get(f"{BASE_URL}/users/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------- PLACES TESTS -----------------

def test_get_place(test_place):
    response = requests.get(f"{BASE_URL}/places/{test_place}")
    assert response.status_code == 200
    assert response.json()["id"] == test_place

def test_list_places():
    response = requests.get(f"{BASE_URL}/places/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------- REVIEWS TESTS -----------------

def test_get_review(test_review):
    response = requests.get(f"{BASE_URL}/reviews/{test_review}")
    assert response.status_code == 200
    assert response.json()["id"] == test_review

def test_list_reviews():
    response = requests.get(f"{BASE_URL}/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_review(test_review):
    response = requests.delete(f"{BASE_URL}/reviews/{test_review}")
    assert response.status_code == 200
    response = requests.get(f"{BASE_URL}/reviews/{test_review}")
    assert response.status_code == 404

# ----------------- AMENITIES TESTS -----------------

def test_get_amenity(test_amenity):
    response = requests.get(f"{BASE_URL}/amenities/{test_amenity}")
    assert response.status_code == 200
    assert response.json()["id"] == test_amenity

def test_list_amenities():
    response = requests.get(f"{BASE_URL}/amenities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)