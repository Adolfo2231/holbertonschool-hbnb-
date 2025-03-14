from app import db, bcrypt
from sqlalchemy.orm import validates
from .base_model import BaseModel  # Import BaseModel from its module
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """Ensure names have valid length."""
        if not name or len(name) < 3 or len(name) > 50:
            raise ValueError(f"{key.replace('_', ' ').title()} must be between 3 and 50 characters.")
        return name

    @validates('email')
    def validate_email(self, key, email):
        """Ensure email format is valid."""
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        return email

    @validates('password')
    def validate_password(self, key, password):
        """
        Ensure the password meets security requirements:
        - At least 8 characters.
        - Contains at least one uppercase letter.
        - Contains at least one number.
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")

        return password

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(self.validate_password('password', password)).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self, exclude_password=True):
        """
        Convert the User object into a dictionary, optionally excluding the password.

        Parameters:
        - exclude_password (bool): If True, the password field will not be included.

        Returns:
        - dict: Dictionary representation of the user.
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
            user_dict["password"] = self.password  # Only include if explicitly requested

        return user_dict