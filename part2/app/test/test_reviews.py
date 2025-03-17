import unittest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from app.api.v1.reviews import api as reviews_api  # Importing the reviews API

class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(reviews_api, path="/reviews")
        self.client = self.app.test_client()

    @patch("app.routes.reviews.facade.create_review")
    def test_create_review_success(self, mock_create_review):
        mock_create_review.return_value = {
            "id": "1",
            "text": "Great place!",
            "rating": 5,
            "user_id": "123",
            "place_id": "456"
        }
        with self.app.app_context():
            response = self.client.post("/reviews/", json={
                "text": "Great place!",
                "rating": 5,
                "user_id": "123",
                "place_id": "456"
            })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    @patch("app.routes.reviews.facade.create_review")
    def test_create_review_invalid_data(self, mock_create_review):
        mock_create_review.return_value = {"error": "Invalid input data"}
        with self.app.app_context():
            response = self.client.post("/reviews/", json={
                "text": "",
                "rating": 10,
                "user_id": "",
                "place_id": "456"
            })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    @patch("app.routes.reviews.facade.get_review")
    def test_get_review_success(self, mock_get_review):
        mock_get_review.return_value = {
            "id": "1",
            "text": "Nice place",
            "rating": 4,
            "user_id": "123",
            "place_id": "456"
        }
        with self.app.app_context():
            response = self.client.get("/reviews/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], "1")

    @patch("app.routes.reviews.facade.get_review")
    def test_get_review_not_found(self, mock_get_review):
        mock_get_review.return_value = None
        with self.app.app_context():
            response = self.client.get("/reviews/99")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)

    @patch("app.routes.reviews.facade.update_review")
    def test_update_review_success(self, mock_update_review):
        mock_update_review.return_value = {
            "id": "1",
            "text": "Updated review",
            "rating": 5,
            "user_id": "123",
            "place_id": "456"
        }
        with self.app.app_context():
            response = self.client.put("/reviews/1", json={
                "text": "Updated review",
                "rating": 5,
                "user_id": "123",
                "place_id": "456"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["text"], "Updated review")

    @patch("app.routes.reviews.facade.delete_review")
    def test_delete_review_success(self, mock_delete_review):
        mock_delete_review.return_value = True
        with self.app.app_context():
            response = self.client.delete("/reviews/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

    @patch("app.routes.reviews.facade.get_reviews_by_place")
    def test_get_reviews_by_place(self, mock_get_reviews_by_place):
        mock_get_reviews_by_place.return_value = [
            {"id": "1", "text": "Nice place", "rating": 4, "user_id": "123", "place_id": "456"},
            {"id": "2", "text": "Awesome stay", "rating": 5, "user_id": "124", "place_id": "456"}
        ]
        with self.app.app_context():
            response = self.client.get("/reviews/places/456/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

if __name__ == "__main__":
    unittest.main()