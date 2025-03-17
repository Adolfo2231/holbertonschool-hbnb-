"""
Amenities API Module

This module defines API endpoints for amenity operations.
Regular users can only view amenities, while creation and management
is restricted to administrators.

Features:
- Public amenity viewing
- Admin-only amenity management
- Structured exception handling
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.amenity import Amenity
from flask_jwt_extended import jwt_required
from flask import request
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, InternalServerError

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        if not api.payload or "name" not in api.payload:
            return {'error': 'Missing required field: name'}, 400

        amenity = facade.create_amenity(api.payload)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return amenity.to_dict(), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve all amenities (Public access)."""
        try:
            amenities = facade.get_all_amenities()
            return {
                "status": "success",
                "data": [amenity.to_dict() for amenity in amenities]
            }, 200
        except Exception as e:
            raise InternalServerError(str(e))


class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        """Create a new amenity (Admins Only)."""
        if not is_admin():
            return {"error": "Admin privileges required"}, 403

        amenity_data = request.get_json()
        result = facade.create_amenity(amenity_data)

        if isinstance(result, tuple):
            return result

        return result, 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200


class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        """Modify an amenity (Admins Only)."""
        if not is_admin():
            return {"error": "Admin privileges required"}, 403

        update_data = request.get_json()
        result = facade.update_amenity(amenity_id, update_data)

        return result, 200


@api.route('/place/<place_id>/amenities')
class PlaceAmenities(Resource):
    def get(self, place_id):
        try:
            # Usar get_amenities_by_place del repositorio
            amenities = facade.get_amenities_by_place(place_id)
            return {
                "status": "success",
                "data": [amenity.to_dict() for amenity in amenities]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 500
