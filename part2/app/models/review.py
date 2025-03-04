"""
Review model module for the HBnB application.

This module defines the Review class which represents user reviews for places.
Each review includes text content, a numerical rating, and references to both
the user who created it and the place being reviewed.
"""

from app.models.base_model import BaseModel
from app.services import facade


class Review(BaseModel):
    def __init__(self, text: str, rating: int, user_id: str, place_id: str):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.user_id = user_id
        self.place_id = place_id

    def validate_text(self, text: str) -> str:
        if not text:
            raise ValueError("Text cannot be empty")
        if len(text) > 300:
            raise ValueError("Text must be less than 300 characters")
        return text

    def validate_rating(self, rating):
        """Ensure the rating is between 1 and 5."""
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def to_dict(self):
        """Convert review object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
