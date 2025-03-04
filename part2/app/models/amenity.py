"""
Amenity model module for the HBnB application.

This module defines the Amenity class, which represents the amenities
available at a place. Amenities are features or services that enhance
the comfort or convenience of a place, such as Wi-Fi, air conditioning,
or a swimming pool.
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Class representing an amenity in the HBnB application."""

    def __init__(self, name: str):
        """Initialize an Amenity instance."""
        super().__init__()
        self.name = self.validate_name(name)
        self.places = []  # Lista de lugares que tienen esta amenidad

    def validate_name(self, name: str) -> str:
        """
        Validate the name of the amenity.

        Args:
            name (str): The name of the amenity to validate.

        Returns:
            str: The validated name.

        Raises:
            ValueError: If the name is empty or exceeds 50 characters.
        """
        if not name:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        return name

    def validate_place(self, place) -> None:
        # Importación diferida para evitar el ciclo
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("El objeto debe ser una instancia de Place")
        self.places.append(place)
        place.add_amenity(self)
