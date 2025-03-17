import unittest
from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestModels(unittest.TestCase):
    """Test case for verifying models functionality."""

    def setUp(self):
        """Initialize a fresh test database before each test."""
        db.create_all()

    def tearDown(self):
        """Clean up the test database after each test."""
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        """Test user creation and validation."""
        user = User(first_name="John", last_name="Doe", email="john@example.com", password="SecurePass123")
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(email="john@example.com").first())

    def test_create_place(self):
        """Test place creation and relationship with user."""
        user = User(first_name="Alice", last_name="Smith", email="alice@example.com", password="StrongPass123")
        db.session.add(user)
        db.session.commit()

        place = Place(title="Cozy Cabin", description="A nice place in the woods", price=100.0,
                      latitude=45.0, longitude=-120.0, owner_id=user.id)
        db.session.add(place)
        db.session.commit()
        self.assertEqual(user.places[0].title, "Cozy Cabin")

    def test_create_review(self):
        """Test review creation and relationship with place and user."""
        user = User(first_name="Mike", last_name="Jordan", email="mike@example.com", password="M1keP@ss")
        place = Place(title="Luxury Villa", description="High-end place", price=500.0,
                      latitude=50.0, longitude=-130.0, owner_id="12345")
        db.session.add_all([user, place])
        db.session.commit()

        review = Review(text="Amazing stay!", rating=5, user_id=user.id, place_id=place.id)
        db.session.add(review)
        db.session.commit()
        self.assertEqual(place.reviews[0].text, "Amazing stay!")

    def test_create_amenity(self):
        """Test amenity creation and relationship with places."""
        place = Place(title="Beach House", description="Great ocean view", price=250.0,
                      latitude=30.0, longitude=-100.0, owner_id="67890")
        amenity = Amenity(name="Wi-Fi")
        db.session.add_all([place, amenity])
        db.session.commit()

        place.amenities.append(amenity)
        db.session.commit()
        self.assertIn(amenity, place.amenities)

    def test_invalid_user_email(self):
        """Test invalid email format."""
        with self.assertRaises(ValueError):
            User(first_name="Invalid", last_name="User", email="invalid-email", password="Pass1234")

    def test_invalid_price(self):
        """Test invalid price validation in Place."""
        with self.assertRaises(ValueError):
            Place(title="Cheap Place", description="Too cheap", price=-10.0,
                  latitude=20.0, longitude=-90.0, owner_id="12345")

    def test_invalid_rating(self):
        """Test invalid rating validation in Review."""
        with self.assertRaises(ValueError):
            Review(text="Bad rating", rating=10, user_id="123", place_id="456")

if __name__ == "__main__":
    unittest.main()
