#!/usr/bin/env python3

"""
Place model module for the HBnB application.

This module defines the Place class which represents accommodations or
locations that can be listed in the application. Each place has attributes
such as title, description, price, geographical coordinates, and is associated
with an owner. Places can also have amenities and reviews.
"""

from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(
            self,
            title: str,
            description: str,
            price: float,
            latitude: float,
            longitude: float,
            owner_id: User,
            amenities=None):
        """
        Initialize a Place instance.
        """
        super().__init__()
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = self.validate_owner(owner_id)
        self.amenities = amenities if amenities else []
        self.reviews = []

    def validate_title(self, title: str) -> str:
        """
        Validate the title of the place.
        """
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
        return title

    def validate_price(self, price: float) -> float:
        """
        Validate the price of the place.
        """
        if price <= 0 or price is None:
            raise ValueError("Price must be greater than 0")
        return price

    def validate_latitude(self, latitude: float) -> float:
        """
        Validate the latitude of the place.
        """
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    def validate_longitude(self, longitude: float) -> float:
        """
        Validate the longitude of the place.
        """
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    def validate_description(self, description: str) -> str:
        """Validar descripción"""
        if description and len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        return description

    def validate_owner(self, owner_id: str) -> User:
        """
        Validate the owner of the place.
        """
        if not owner_id:
            raise ValueError("Owner cannot be empty")

        # Solo validamos que sea una instancia de User
        if not isinstance(owner_id, User):
            raise ValueError("Owner must be a User instance")

        return owner_id

    def add_review(self, review) -> None:
        """Add a review to the place."""
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Only Review instances can be added.")
        self.reviews.append(review)
        review.place = self

    def add_amenity(self, amenity) -> None:
        """Add an amenity to the place."""
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Only Amenity instances can be added.")
        self.amenities.append(amenity)

    def to_dict(self):
        """Convert instance attributes to a
        dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id.id if isinstance(self.owner_id, User)
            else self.owner_id,
            "amenities": self.amenities
        }
