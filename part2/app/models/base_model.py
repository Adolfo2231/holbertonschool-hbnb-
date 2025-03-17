"""
BaseModel module for the HBnB application.

This module defines the BaseModel class as a SQLAlchemy model.
"""

from app.extensions import db  # Importar la instancia de SQLAlchemy
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """Base class for all models in the HBnB application."""

    __abstract__ = True  # Evita que SQLAlchemy cree una tabla para BaseModel

    # Definición de columnas comunes para todos los modelos
    id = db.Column(
        db.String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime, 
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def save(self):
        """Save the instance to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, data):
        """Update object attributes from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Delete the instance from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

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
