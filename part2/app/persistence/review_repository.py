from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        """Initialize ReviewRepository with the Review model."""
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        return self.model.query.filter_by(place_id=place_id).all()

    def get_reviews_by_user(self, user_id):
        """Get all reviews by a specific user."""
        return self.model.query.filter_by(user_id=user_id).all()

    def get_average_rating(self, place_id):
        """Get average rating for a place."""
        result = db.session.query(db.func.avg(self.model.rating))\
            .filter_by(place_id=place_id).scalar()
        return float(result) if result else 0.0 