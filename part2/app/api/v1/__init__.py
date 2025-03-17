#!/usr/bin/env python3
"""Initialize API v1 Blueprint"""

from flask_restx import Api
from flask import Blueprint

# Crear el Blueprint para la API v1
blueprint = Blueprint('api_v1', __name__)
api = Api(blueprint, version='1.0', title='HBnB API', description='HolbertonBnB REST API')

# Importar los namespaces
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns

# Agregar los namespaces a la API
api.add_namespace(reviews_ns, path='/api/v1/reviews')
api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(auth_ns, path='/api/v1/auth')
