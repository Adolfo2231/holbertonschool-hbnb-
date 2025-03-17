from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        """Initialize PlaceRepository with the Place model."""
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Get all places for a specific owner."""
        return self.model.query.filter_by(owner_id=owner_id).all()

    def get_places_by_price_range(self, min_price, max_price):
        """Get places within a price range."""
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all() 