"""
User Model

This module defines the User model for the HBnB application. It represents
users within the system, including authentication, validation, and data
management.

This model can be used both with SQLAlchemy as a database-backed model or as
an independent object in Python applications.

Features:
- Validation for first name, last name, email, and password.
- Secure password hashing and authentication.
- Relationship handling with places and reviews via SQLAlchemy.
- Conversion of instance attributes to dictionaries for serialization.
- Allows temporary local storage for users when not using a database.

Attributes:
    first_name (str): The first name of the user (required, max 50 chars).
    last_name (str): The last name of the user (required, max 50 chars).
    email (str): The unique email address of the user (required, max 120 chars).
    password (str): The hashed password of the user (required).
    is_admin (bool): Indicates whether the user has admin privileges (default: False).
    places (relationship): Relationship with Place, linking the places owned by the user.
    reviews (relationship): Relationship with Review, linking the reviews written by the user.
"""

from app import db, bcrypt
from sqlalchemy.orm import relationship, validates
from .base_model import BaseModel
import re
from typing import Dict, Any, List

class User(BaseModel):
    """User model class for handling user data, authentication, and relationships."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # SQLAlchemy relationships
    places = relationship('Place', backref='owner', lazy=True)
    reviews = relationship('Review', backref='user', lazy=True)

    def __init__(
        self, first_name: str, last_name: str, email: str, password: str,
        is_admin: bool = False, **kwargs: Any
    ) -> None:
        """
        Initialize a User instance with validation.
        
        Args:
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            email (str): Email address of the user.
            password (str): Raw password that will be validated and hashed.
            is_admin (bool, optional): Whether the user is an admin. Defaults to False.
        """
        self.first_name = self.validate_name("first_name", first_name)
        self.last_name = self.validate_name("last_name", last_name)
        self.email = self.validate_email("email", email)
        self.is_admin = is_admin

        if password:
            self.password = self.validate_password("password", password)
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

        super().__init__(**kwargs)

    @validates('password')
    def validate_password(self, key: str, password: str) -> str:
        """
        Validate password complexity requirements.
        """
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")
        return password

    @validates('first_name', 'last_name')
    def validate_name(self, key: str, name: str) -> str:
        """
        Validate name fields.
        """
        if not isinstance(name, str):
            raise TypeError(f"{key.replace('_', ' ').title()} must be a string.")
        if not name or len(name) < 3 or len(name) > 50:
            raise ValueError(f"{key.replace('_', ' ').title()} must be between 3 and 50 characters.")
        return name

    @validates('email')
    def validate_email(self, key: str, email: str) -> str:
        """
        Validate email format.
        """
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        return email

    def verify_password(self, password: str) -> bool:
        """
        Verify if a given password matches the stored hashed password.
        """
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self, exclude_password: bool = True) -> Dict[str, Any]:
        """
        Convert the User object into a dictionary representation.
        """
        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        if not exclude_password:
            user_dict["password"] = self.password

        return user_dict
