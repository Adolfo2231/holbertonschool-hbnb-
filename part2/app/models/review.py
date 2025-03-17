"""
Review Model

This module defines the Review model for the HBnB application. It represents
user-generated reviews associated with places. Each review has a rating, text,
and is linked to a user and a place.

This model can be used both with SQLAlchemy as a database-backed model or
independently in-memory for temporary storage.

Features:
- Validation for text content and rating.
- Supports both database persistence and in-memory usage during runtime.
- Establishes a relationship with User as the author of each review.
- Establishes a relationship with Place as the target of each review.

Attributes:
    text (str): The text content of the review (required, max 1000 chars).
    rating (int): Rating score (1 to 5, required).
    user_id (str): The ID of the user who wrote the review (required).
    place_id (str): The ID of the place being reviewed (required).
    author (relationship): SQLAlchemy relationship to link Review to User.
    place (relationship): SQLAlchemy relationship to link Review to Place.
"""

from app.models.base_model import BaseModel
from sqlalchemy.orm import validates, relationship
from app import db
from typing import Dict, Any

class Review(BaseModel):
    """Review model class for handling review data and its validation."""
    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __init__(
        self, text: str, rating: int, user_id: str, place_id: str, **kwargs: Any
    ):
        """
        Initialize a Review instance with validation.
        """
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @validates('text')
    def validate_text(self, key: str, text: str) -> str:
        """Validate the review text content."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string")
        if len(text) > 1000:
            raise ValueError("Review text must be 1000 characters or less")
        return text.strip()

    @validates('rating')
    def validate_rating(self, key: str, rating: int) -> int:
        """Validate the review rating."""
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    @validates('user_id')
    def validate_user_id(self, key: str, user_id: str) -> str:
        """Validate the user ID."""
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a valid string")
        return user_id

    @validates('place_id')
    def validate_place_id(self, key: str, place_id: str) -> str:
        """Validate the place ID."""
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Place ID must be a valid string")
        return place_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert instance attributes to a dictionary for serialization."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
