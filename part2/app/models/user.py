#! /usr/bin/env python3

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
import uuid
from datetime import datetime


class User:
    """
    Class to represent a user.

    Attributes:
    ----------
    id : str
        Unique identifier for the user.
    first_name : str
        User's first name.
    last_name : str
        User's last name.
    email : str
        User's email address.
    __password : bytes
        Hash of the user's password.
    is_admin : bool
        Indicates if the user has admin privileges.
    created_at : datetime
        User's creation date.
    updated_at : datetime
        Date of the last update to the user.
    """

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 email: str,
                 password: str,
                 is_admin: bool =
                 False):
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
        self.id = str(uuid.uuid4())
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.__password = self.hash_password(password)
        self.is_admin = is_admin
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def validate_name(self, name: str, field_name: str) -> str:
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
        if len(name) > 50:
            raise ValueError(f"{field_name} must be 50 characters or less")
        return name

    def validate_email(self, email: str) -> str:
        """
        Validates the email format.

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
            If the email format is invalid.
        """
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        else:
            raise ValueError("Invalid email format")

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

    def update(self, first_name: str = None, last_name: str = None,
               email: str = None, is_admin: bool = None):
        """
        Updates the user's details.

        Parameters:
        -----------
        first_name : str, optional
            New first name for the user.
        last_name : str, optional
            New last name for the user.
        email : str, optional
            New email address for the user.
        is_admin : bool, optional
            New admin status for the user.
        """
        if first_name:
            self.first_name = self.validate_name(first_name, "First name")
        if last_name:
            self.last_name = self.validate_name(last_name, "Last name")
        if email:
            self.email = self.validate_email(email)
        if is_admin is not None:
            self.is_admin = is_admin
        self.updated_at = datetime.now()
