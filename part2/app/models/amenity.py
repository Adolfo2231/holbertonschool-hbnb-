"""
Amenity Model

This module defines the Amenity model for the HBnB application. It represents
facilities or services that a Place can offer, such as Wi-Fi, pool, parking,
etc.

This model can be used both with SQLAlchemy as a database-backed model or
independently in-memory for temporary storage.

Features:
- Validation for amenity name.
- Supports both database persistence and in-memory usage during runtime.
- Establishes a Many-to-Many relationship with Place.

Attributes:
    name (str): The name of the amenity (required, unique, max 100 chars).
    places (relationship): Many-to-Many relationship with Place.
"""

from app.models.base_model import BaseModel
from sqlalchemy.orm import validates, relationship
from app import db
from typing import Dict, Any
from app.models.place import place_amenity

class Amenity(BaseModel):
    """Amenity model class for handling amenity data and its validation."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False, unique=True)

    # Establish Many-to-Many relationship with Place
    places = relationship('Place', secondary=place_amenity, back_populates='amenities', lazy=True)

    def __init__(self, name: str, **kwargs: Any):
        """
        Initialize an Amenity instance with validation.
        """
        super().__init__(**kwargs)
        self.name = self.validate_name(name)

    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """Validate the amenity name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name must be a non-empty string")
        if len(name) > 100:
            raise ValueError("Amenity name must be 100 characters or less")
        return name.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Convert instance attributes to a dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
            } 
