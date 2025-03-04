"""
This module defines the User class for managing users in an application.

The User class includes functionalities to:
- Create a new user with a unique identifier.
- Validate names and email addresses.
- Hash and verify passwords securely.
- Update user details.
"""

import re
import bcrypt
from datetime import datetime
from app.models.base_model import BaseModel
from app.services import facade


class User(BaseModel):
    """
    Class to represent a user.

    Attributes:
    ----------
    id : str
        Unique identifier for the user.
    username : str
        User's username.
    first_name : str
        User's first name.
    last_name : str
        User's last name.
    email : st
        User's email address.
    __password : bytes
        Hash of the user's password.
    is_admin : bool
        Indicates if the user has admin privileges.
    created_at : datetime
        User's creation date.
    updated_at : datetime
        Date of the last update to the user.
    places : list
        List of places owned by the user.
    facade : HBnBFacade
        Instance of the HBnBFacade for interacting with repositories.
    """

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 email: str,
                 # password: str = None,
                 is_admin: bool = False):
        """
        Initializes a new user with the provided details.

        Parameters:
        -----------
        first_name : str
            User's first name.
        last_name : str
            User's last name.
        email : str
            User's email address.
        password : str
            User's password.
        is_admin : bool, optional
            Indicates if the user is an admin (default is False).
        """
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        # self.validate_password(password)
        # self.__password = self.hash_password(password)
        # hash
        self.is_admin = is_admin
        self.places = []

    def validate_name(self, name: str) -> str:
        """
        Validates that the name does not exceed 50 characters.

        Parameters:
        -----------
        name : str
            Name to validate.
        field_name : str
            Field name for the error message.

        Returns:
        --------
        str
            The validated name.

        Raises:
        ------
        ValueError
            If the name exceeds 50 characters.
        """
        if not name:
            raise ValueError("Name cannot be empty")
        elif len(name) < 3 or len(name) > 50:
            raise ValueError(
                f"{len(name)} must be 3 char min or 50 char or less")
        return name

    def validate_email(self, email: str) -> str:
        """
        Validates the email format and uniqueness.

        Parameters:
        -----------
        email : str
            Email to validate.

        Returns:
        --------
        str
            The validated email.

        Raises:
        ------
        ValueError
            If the email format is invalid or if the email already exists.
        """
        if not email:
            raise ValueError("Email cannot be empty")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    def validate_password(self, password: str) -> str:
        """Validar complejidad de contraseña"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            raise ValueError(
                "Password must contain at least one letter and one number")
        return password

    def hash_password(self, password: str) -> bytes:
        """
        Generates a secure hash for the password.

        Parameters:
        -----------
        password : str
            Password to hash.

        Returns:
        --------
        bytes
            Hash of the password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the stored hash.

        Parameters:
        -----------
        password : str
            Password to verify.

        Returns:
        --------
        bool
            True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.__password)

    def is_administrator(self) -> bool:
        """
        Check if the user has administrator privileges.

        Returns:
        --------
        bool
            True if the user is an administrator, False otherwise.
        """
        return self.is_admin

    def add_place(self, place):
        """Adds a place to the user's list of owned places."""
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("Only Place instances can be added.")

        # Verificar que el lugar no tenga ya un propietario
        if place in self.places:
            raise ValueError("Place already added to this user")

        self.places.append(place)
        # Aseguramos la relación bidireccional
        if place.owner != self:
            place.owner = self
