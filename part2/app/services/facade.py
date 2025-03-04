#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade that provides a unified interface
    to interact with the application repositories."""

    def __init__(self):
        """Initialize in-memory repositories for each model."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Create a new user.

        Args:
            user_data (dict): User data to create

        Returns:
            User: Created user object or error message
        """
        if not isinstance(user_data, dict):
            return {"error": "Invalid user data format"}, 400

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Get a user by ID.

        Args:
            user_id (str): ID of the user to find

        Returns:
            User: Found user object or None
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Get a user by email.

        Args:
            email (str): Email of the user to find

        Returns:
            User: Found user object or None
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Get all users.

        Returns:
            list: List of all users
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Update an existing user.

        Args:
            user_id (str): ID of the user to update
            user_data (dict): Updated user data

        Returns:
            User: Updated user object or None
        """
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            return user
        return None

    def create_amenity(self, amenity_data):
        """
        Create a new amenity.

        Args:
            amenity_data (dict): Amenity data to create

        Returns:
            Amenity: Created amenity object
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Get an amenity by ID.

        Args:
            amenity_id (str): ID of the amenity to find

        Returns:
            Amenity: Found amenity object or None
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Get all amenities.

        Returns:
            list: List of all amenities
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.

        Args:
            amenity_id (str): ID of the amenity to update
            amenity_data (dict): Updated amenity data

        Returns:
            Amenity: Updated amenity object or None
        """
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            return amenity
        return None

    def create_place(self, place_data):
        # ✅ Retrieve User object from `owner_id`
        user = self.get_user(place_data["owner_id"])
        if not user:
            return {"error": "Owner not found"}, 400

        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=user,
        amenities=place_data.get("amenities", [])
    )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Get a place by ID.

        Args:
            place_id (str): ID of the place to find

        Returns:
            Place: Found place object or None
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Get all places.

        Returns:
            list: List of all places
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update an existing place.

        Args:
            place_id (str): ID of the place to update
            place_data (dict): Updated place data

        Returns:
            Place: Updated place object or None
        """
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
            return place
        return None

    def create_review(self, review_data):
        """
        Create a new review after validating the data.

        Args:
            review_data (dict): Review data to create

        Returns:
            Review: Created review object or error message
        """
        required_fields = ["text", "rating", "user_id", "place_id"]

        for field in required_fields:
            if field not in review_data:
                return {"error": f"Missing required field: {field}"}, 400

        user = self.get_user(review_data["user_id"])
        place = self.get_place(review_data["place_id"])

        if not user:
            return {"error": "User not found"}, 404
        if not place:
            return {"error": "Place not found"}, 404

        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user_id=review_data["user_id"],
            place_id=review_data["place_id"]
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Get a review by ID.

        Args:
            review_id (str): ID of the review to find

        Returns:
            Review: Found review object or None
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Get all reviews.

        Returns:
            list: List of all reviews
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place.

        Args:
            place_id (str): ID of the place to get reviews for

        Returns:
            list: List of reviews for the specified place
        """
        return [review for review in self.review_repo.get_all()
                if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """
        Update an existing review.

        Args:
            review_id (str): ID of the review to update
            review_data (dict): Updated review data

        Returns:
            Review: Updated review object or None
        """
        review = self.review_repo.get(review_id)
        if review:
            review.update(review_data)
            return review
        return None

    def delete_review(self, review_id):
        """
        Delete an existing review.

        Args:
            review_id (str): ID of the review to delete

        Returns:
            bool: True if successfully deleted, None if not found
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return True
