from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        """Initialize AmenityRepository with the Amenity model."""
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Get amenity by name."""
        return self.model.query.filter_by(name=name).first()

    def get_amenities_by_place(self, place_id):
        """Get all amenities for a specific place."""
        return self.model.query\
            .join(self.model.places)\
            .filter_by(id=place_id)\
            .all() 