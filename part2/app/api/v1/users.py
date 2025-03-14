"""
Users API module for the HBnB application.

This module defines the API endpoints for user operations, including
creating, retrieving, updating, and listing users. It uses Flask-RESTx
to define the routes and handle HTTP requests, providing a RESTful
interface for user management.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Initialize Bcrypt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    """
    Resource for creating and listing users.

    Methods:
        post: Create a new user.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user."""
        user_data = api.payload

        try:
            # Validate required fields
            if not all([user_data['first_name'],
                        user_data['last_name'],
                       user_data['email'],
                       user_data['password']]):
                return {"error": "Missing required fields"}, 400

            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email}, 201

        except ValueError as e:
            return {"error": str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for retrieving and updating a specific user.

    Methods:
        get: Retrieve user details by ID.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        print(f"User: {user}")
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200


@api.route('/all')
class UserListAll(Resource):
    """
    Resource for listing all users.

    Methods:
        get: Retrieve all users.
    """

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get all users."""
        users = facade.get_all_users()
        # Now `to_dict()` ensures clean JSON
        return [user.to_dict() for user in users], 200


@api.route('/update/<user_id>')
class UserResource(Resource):
    """
    Resource for updating a specific user.

    Methods:
        put: Update user details.
    """

    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details."""
        user_data = api.payload
        user = facade.update_user(user_id, user_data)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
