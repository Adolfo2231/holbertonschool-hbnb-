"""
Reviews API module for the HBnB application.

This module defines the API endpoints for review operations, including
creating, retrieving, updating, and deleting reviews. It uses Flask-RESTx
to define the routes and handle HTTP requests, providing a RESTful
interface for review management.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, InternalServerError

api = Namespace('reviews', description='Review operations')

# Define models for input validation and documentation
user_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'username': fields.String(description='Username')
})

amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user': fields.Nested(user_model, description='User who wrote the review')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           description='List of reviews')
})


@api.route('/')
class ReviewList(Resource):
    """
    Resource for creating and listing reviews.

    Methods:
        post: Create a new review.
    """

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review."""
        data = request.get_json()
        current_user_id = get_jwt_identity()

        place = facade.get_place(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 404

        # Prevent users from reviewing their own place
        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place"}, 400

        # Check for duplicate reviews
        existing_review = facade.get_review_by_user_and_place(
            current_user_id, place.id)
        if existing_review:
            return {"error": "You have already reviewed this place"}, 400

        new_review = Review(
            user_id=current_user_id,
            place_id=place.id,
            text=data["text"]
        )

        saved_review = facade.create_review(new_review)
        return saved_review.to_dict(), 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource for retrieving, updating, and deleting a specific review.

    Methods:
        get: Retrieve review details by ID.
        put: Update a review's information.
        delete: Delete a review.
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(403, "Permission denied")
    @api.response(404, "Review not found")
    def put(self, review_id: str) -> dict:
        """Update review (Only authors can modify their reviews)."""
        try:
            current_user_id = get_jwt_identity()
            review = facade.get_review(review_id)

            if not review:
                raise NotFound("Review not found")

            if review.user_id != current_user_id:
                raise Forbidden("Users can only modify their own reviews")

            update_data = request.get_json()
            result = facade.update_review(review_id, update_data)
            return {"status": "success", "data": result}, 200
        except Exception as e:
            raise InternalServerError(str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid review ID format')
    def delete(self, review_id):
        """Delete a review."""
        try:
            uuid.UUID(review_id)  # Validate format
        except ValueError:
            return {"error": "Invalid review ID format"}, 400

        deleted = facade.delete_review(review_id)
        if deleted is None:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as e:
            return {"error": str(e)}, 500
