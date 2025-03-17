import unittest
import json
from app import create_app

class PlaceTestCase(unittest.TestCase):
    """Test cases for the Place API"""
    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client before all tests"""
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Ensure at least one place exists before running tests
        response = cls.client.post('/api/v1/places/', 
                                    data=json.dumps({
                                    "title": "Test Place",
                                    "description": "For testing",
                                    "price": 50.00,
                                    "latitude": 12.34,
                                    "longitude": 56.78,
                                    "owner_id": "123",
                                    "amenities": ["wifi"]
                                    }),
                                    content_type='application/json')
        if response.status_code != 201:
            raise Exception("Test setup failed: Could not create test place")



    def test_create_place_invalid(self):
        """Test trying to create a place with missing fields"""
        response = self.client.post('/api/v1/places/', 
                                    data=json.dumps({
                                        "title": "Invalid Place"
                                    }),  # Missing required fields
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
        """Test retrieving all places (GET /api/v1/places/)"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)  # At least 1 place exists

    def test_get_place_by_id(self):
        """Test retrieving a single place by ID (GET /api/v1/places/{place_id})"""
        response = self.client.get('/api/v1/places/')
        place_id = response.json[0]['id']  # Get the first place

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], place_id)

    def test_get_nonexistent_place(self):
        """Test retrieving a non-existing place (GET /api/v1/places/{invalid_id})"""
        response = self.client.get('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Place not found")

    def test_update_place(self):
        """Test updating a place (PUT /api/v1/places/{place_id})"""
        response = self.client.get('/api/v1/places/')
        place_id = response.json[0]['id']  # Get the first place

        response = self.client.put(f'/api/v1/places/{place_id}', 
                                   data=json.dumps({
                                       "title": "Updated Apartment",
                                       "description": "Now with a better view!",
                                       "price": 120.00,
                                       "latitude": 40.7308,
                                       "longitude": -73.9973,
                                       "owner_id": "123",
                                       "amenities": ["wifi", "gym"]
                                   }),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], "Updated Apartment")

    def test_update_nonexistent_place(self):
        """Test updating a non-existing place (PUT /api/v1/places/{invalid_id})"""
        response = self.client.put('/api/v1/places/invalid_id', 
                                   data=json.dumps({
                                       "title": "Test",
                                       "price": 100.00
                                   }),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Place not found")

if __name__ == '__main__':
    unittest.main()
