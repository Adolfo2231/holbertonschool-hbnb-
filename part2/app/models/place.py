"""
Place Model

This module defines the Place model for the HBnB application. It represents
accommodations or locations that can be listed in the system. Each place has
attributes such as title, description, price, geographical coordinates, and
an associated owner.

This model can be used both with SQLAlchemy as a database-backed model or
independently in-memory for temporary storage.

Features:
- Validation for title, description, price, latitude, and longitude.
- Ability to manage associated amenities and reviews.
- Supports both database persistence and in-memory usage during runtime.
- Establishes a relationship with User as the owner of each Place.

Attributes:
    title (str): The title of the place (required, max 100 chars).
    description (str): A description of the place (optional, max 1000 chars).
    price (float): The price per night (required, must be positive).
    latitude (float): The latitude of the place (required, -90 to 90).
    longitude (float): The longitude of the place (required, -180 to 180).
    owner_id (str): The ID of the owner (required, must be a valid user ID).
    owner (relationship): SQLAlchemy relationship to link Place to User.
    reviews (relationship): Relationship with Review.
    amenities (relationship): Many-to-Many relationship with Amenity.
"""

from app.models.base_model import BaseModel
from sqlalchemy.orm import validates, relationship
from app import db
from typing import Dict, Any

# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True, extend_existing=True)
)

class Place(BaseModel):
    """Place model class for handling place data and its validation."""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Establish relationships 
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=place_amenity, back_populates='places', lazy=True)

    def __init__(
        self, title: str, description: str, price: float, latitude: float,
        longitude: float, owner_id: str, **kwargs: Any
    ):
        """
        Initialize a Place instance with validation.
        """
        super().__init__(**kwargs)
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = self.validate_owner(owner_id)

    @validates('title')
    def validate_title(self, key: str, title: str) -> str:
        """Validate the title of the place."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
        return title.strip()

    @validates('price')
    def validate_price(self, key: str, price: float) -> float:
        """Validate the price of the place."""
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        return float(price)

    @validates('latitude')
    def validate_latitude(self, key: str, latitude: float) -> float:
        """Validate the latitude of the place."""
        if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return float(latitude)

    @validates('longitude')
    def validate_longitude(self, key: str, longitude: float) -> float:
        """Validate the longitude of the place."""
        if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return float(longitude)

    @validates('description')
    def validate_description(self, key: str, description: str) -> str:
        """Validate the description of the place."""
        if description and not isinstance(description, str):
            raise ValueError("Description must be a string")
        if description and len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        return description

    @validates('owner_id')
    def validate_owner(self, key: str, owner_id: str) -> str:
        """Validate the owner ID."""
        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("Owner must be a valid user ID string")
        return owner_id

    def to_dict(self) -> Dict[str, Any]:
        """Convert instance attributes to a dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
