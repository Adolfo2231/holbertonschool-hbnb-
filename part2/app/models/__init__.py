"""
Initialize the models package
"""

# Primero importamos BaseModel ya que no depende de otros modelos
from .base_model import BaseModel

# Luego importamos los modelos en orden de dependencia
from .user import User
from .place import Place
from .amenity import Amenity
from .review import Review

__all__ = [
    'BaseModel',
    'User',
    'Place',
    'Amenity',
    'Review'
]