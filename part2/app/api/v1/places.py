"""
Places API module for the HBnB application.

This module defines the API endpoints for place operations, including
creating, retrieving, updating, and listing places. It uses Flask-RESTx
to define the routes and handle HTTP requests, providing a RESTful
interface for place management.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.models.place import Place
from flask import request
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, InternalServerError
api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    """Resource for creating and listing places."""

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        try:
            data = api.payload

            # Validación básica de campos requeridos
            required_fields = [
                'title',
                'price',
                'latitude',
                'longitude',
                'owner_id',
                'amenities']
            missing_fields = [
                field for field in required_fields if field not in data]

            if missing_fields:
                return {
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }, 400

            result = facade.create_place(data)

            if isinstance(result, dict) and "error" in result:
                return result, 400

            return {
                "status": "success",
                "message": "Place created successfully",
                "data": result
            }, 201

        except ValueError as ve:
            return {
                "status": "error",
                "message": str(ve)
            }, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (Public access)."""
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)

        if min_price and max_price:
            places = facade.get_places_by_price_range(min_price, max_price)
        else:
            places = facade.get_all_places()

        return {"status": "success", "data": [
            place.to_dict() for place in places]}, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Resource for retrieving and updating a specific place."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public access)."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.response(200, "Place updated successfully")
    @api.response(403, "Permission denied")
    @api.response(404, "Place not found")
    def put(self, place_id: str) -> dict:
        """Update place details (Owners and admins can modify places)."""
        try:
            current_user = facade.get_user(get_jwt_identity())
            if not current_user:
                return {"error": "User not found"}, 404

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404

            # Permitir modificación si es admin o dueño del lugar
            if not current_user.is_admin and place.owner_id != current_user.id:
                return {"error": "Unauthorized action"}, 403

            update_data = request.get_json()
            result = facade.update_place(place_id, update_data)
            return {"status": "success", "data": result}, 200
        except Exception as e:
            return {"error": str(e)}, 500


@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            # Verificar que el lugar existe
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Obtener las reviews
            reviews = facade.get_reviews_by_place(place_id)
            return {
                "status": "success",
                "data": {
                    "reviews": [review.to_dict() for review in reviews]
                }
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 500
