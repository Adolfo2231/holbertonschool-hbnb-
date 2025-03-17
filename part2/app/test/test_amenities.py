import unittest
import json
from app import create_app

class AmenityTestCase(unittest.TestCase):
    """Test cases for the Amenity API"""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client before all tests"""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_1_create_amenity(self):
        """Test creating an amenity (POST /api/v1/amenities/)"""
        response = self.client.post('/api/v1/amenities/', 
                                    data=json.dumps({"name": "Pool"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_2_create_amenity_invalid(self):
        """Test trying to create an amenity with missing fields"""
        response = self.client.post('/api/v1/amenities/', 
                                    data=json.dumps({}),  # Missing "name"
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_3_get_amenities(self):
        """Test retrieving all amenities (GET /api/v1/amenities/)"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)  # At least 1 amenity exists

    def test_4_get_amenity_by_id(self):
        """Test retrieving a single amenity by ID (GET /api/v1/amenities/{amenity_id})"""
        response = self.client.get('/api/v1/amenities/')
        amenity_id = response.json[0]['id']  # Get the first amenity

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], amenity_id)

    def test_5_get_nonexistent_amenity(self):
        """Test retrieving a non-existing amenity (GET /api/v1/amenities/{invalid_id})"""
        response = self.client.get('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Amenity not found")

    def test_6_update_amenity(self):
        """Test updating an amenity (PUT /api/v1/amenities/{amenity_id})"""
        response = self.client.get('/api/v1/amenities/')
        amenity_id = response.json[0]['id']  # Get the first amenity

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', 
                                   data=json.dumps({"name": "Updated Pool"}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Pool")

    def test_7_update_nonexistent_amenity(self):
        """Test updating a non-existing amenity (PUT /api/v1/amenities/{invalid_id})"""
        response = self.client.put('/api/v1/amenities/invalid_id', 
                                   data=json.dumps({"name": "Test"}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Amenity not found")

if __name__ == '__main__':
    unittest.main()