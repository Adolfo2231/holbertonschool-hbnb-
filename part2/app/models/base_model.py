"""
BaseModel module for the HBnB application.

This module defines the BaseModel class, which provides common attributes
and methods for other models in the application. It includes functionality
for generating unique IDs and timestamps for creation and updates.
"""

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models in the HBnB application."""

    def __init__(self):
        """Initialize a new BaseModel instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Refresh updated_at timestamp

    def to_dict(self):
        """Convert instance attributes to
        a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __str__(self):
        """Return a string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"
