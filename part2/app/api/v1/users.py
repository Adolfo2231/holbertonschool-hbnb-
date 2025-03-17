"""
Users API Module

This module defines API endpoints for user operations, including
registration, profile management, and account deletion.
Regular users can only manage their own accounts.

Features:
- User registration
- Profile retrieval and updates
- Account deletion
- Structured exception handling
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask import request
from werkzeug.exceptions import BadRequest, Forbidden, Conflict, InternalServerError, NotFound

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(default=False, description='Admin status')
})


@api.route('/')
class UserList(Resource):
    """Resource for creating users."""

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'User already exists')
    @api.response(403, 'Permission denied')
    def post(self):
        """Register a new user."""
        try:
            data = api.payload
            result = facade.create_user(data)
            return {"status": "success", "data": result}, 201

        except ValueError as e:
            raise BadRequest({
                "message": {
                    "status": "error",
                    "message": "Invalid input data",
                    "details": str(e)
                }
            })
        except Conflict as e:
            raise Conflict({
                "message": {
                    "status": "error",
                    "message": "User already exists",
                    "details": str(e)
                }
            })
        except PermissionError as e:
            raise Forbidden({
                "message": {
                    "status": "error",
                    "message": "Permission denied",
                    "details": str(e)
                }
            })
        except Exception as e:
            raise InternalServerError({
                "message": {
                    "status": "error",
                    "message": "Unexpected server error",
                    "details": str(e)
                }
            })


@api.route('/<string:user_id>')
class UserResource(Resource):
    """Resource for retrieving and managing user details."""

    @jwt_required()
    @api.response(200, "User details retrieved successfully")
    @api.response(403, "Permission denied")
    @api.response(404, "User not found")
    def get(self, user_id: str) -> dict:
        """Get user details by ID (Users can only access their own profile)."""
        try:
            if user_id != get_jwt_identity():
                raise Forbidden("Users can only access their own profile")
            user = facade.get_user(user_id)
            return {"status": "success", "data": user.to_dict()}, 200
        except NotFound:
            raise NotFound("User not found")
        except Exception as e:
            raise InternalServerError(str(e))

    @api.expect(user_model, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(403, "Permission denied")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id: str) -> dict:
        """Update user details (Users can modify only their own accounts)."""
        try:
            if user_id != get_jwt_identity():
                raise Forbidden("Users can only modify their own accounts")
            update_data = request.get_json()
            result = facade.update_user(user_id, update_data)
            return {"status": "success", "data": result}, 200
        except NotFound:
            raise NotFound("User not found")
        except ValueError as e:
            raise BadRequest(str(e))
        except Exception as e:
            raise InternalServerError(str(e))

    @api.response(200, "User successfully deleted")
    @api.response(403, "Permission denied")
    @api.response(404, "User not found")
    @jwt_required()
    def delete(self, user_id: str) -> dict:
        """Delete user account (Users can delete only their own accounts)."""
        try:
            current_user_id = get_jwt_identity()
            facade.delete_user(user_id, current_user_id)
            return {"status": "success", "message": "User deleted"}, 200
        except NotFound:
            raise NotFound("User not found")
        except Exception as e:
            raise InternalServerError(str(e))
