#!/usr/bin/env python3

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

# --------------------------------------------
# HBnBFacade Class - Business Logic Layer
# --------------------------------------------


class HBnBFacade:
    """Facade that provides a unified interface to interact with the application repositories."""

    def __init__(self):
        """Initialize repositories for each model."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.amenity_repo = AmenityRepository()
        self.review_repo = ReviewRepository()

    # --------------------------------------------
    # USER MANAGEMENT
    # --------------------------------------------

    def create_user(self, data):
        """Creates a new user ensuring all constraints are met."""
        if self.user_repo.is_email_registered(data["email"]):
            raise ValueError("Email already registered.")

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found.")
        return user

    def update_user(self, user_id, update_data, admin_override=False):
        """Update user details."""
        user = self.get_user(user_id)
        if not admin_override and (
                "email" in update_data or "password" in update_data):
            raise PermissionError("Only admins can modify email or password.")

        for key, value in update_data.items():
            setattr(user, key, value)

        return user.to_dict()

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        user = self.user_repo.get_by_attribute('email', email)
        if not user:
            raise ValueError("User not found.")
        return user

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()
    
    def delete_user(self, user_id, current_user_id):
        """Delete a user by ID."""
        # Toda la lógica de validación aquí
        current_user = self.get_user(current_user_id)
        if not current_user or not current_user.is_admin:
            raise PermissionError("Admin access required")

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
            
        if user.is_admin and self.count_admins() <= 1:
            raise ValueError("Cannot delete the last admin user")

        self.user_repo.delete(user)
        return True

    # --------------------------------------------
    # AMENITY MANAGEMENT
    # --------------------------------------------

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        return amenity

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity."""
        amenity = self.get_amenity(amenity_id)  # Now raises error if not found
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        return amenity

    # --------------------------------------------
    # PLACE MANAGEMENT
    # --------------------------------------------

    def create_place(self, data):
        """Create a new place, ensuring required fields and valid owner/amenities."""
        required_fields = [
            'title',
            'price',
            'latitude',
            'longitude',
            'owner_id',
            'amenities']
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields.")

        owner = self.get_user(data['owner_id'])
        for amenity_id in data['amenities']:
            # This raises an error if the amenity is missing
            self.get_amenity(amenity_id)

        place = Place(**data)
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place."""
        place = self.get_place(place_id)  # Now raises error if not found
        for key, value in place_data.items():
            setattr(place, key, value)
        return place

    # --------------------------------------------
    # REVIEW MANAGEMENT
    # --------------------------------------------

    def create_review(self, review_data):
        """Create a new review."""
        try:
            review = Review(**review_data)
            self.review_repo.add(review)
            return review
        except ValueError as e:
            raise ValueError(f"Validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Internal server error: {str(e)}")

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        return [review for review in self.review_repo.get_all()
                if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update an existing review."""
        review = self.get_review(review_id)  # Now raises error if not found
        for key, value in review_data.items():
            setattr(review, key, value)
        return review

    def delete_review(self, review_id):
        """Delete an existing review."""
        review = self.get_review(review_id)  # Now raises error if not found
        self.review_repo.delete(review)
        return True
