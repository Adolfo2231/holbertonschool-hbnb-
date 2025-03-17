#!/usr/bin/env python3

from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import User, Place, Review, Amenity  # Import your models
from app.extensions import db

class Repository:
    """Base repository class"""
    def __init__(self,model=None):
        self.db = db
        self.model = model

    def get_all(self):
        pass

    def get_by_id(self, id):
        pass

    def add(self, entity):
        pass

    def update(self, entity):
        pass

    def delete(self, id):
        pass

class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of Repository"""
    def __init__(self,model=None):
        super().__init__(model)

    def add(self, entity):
        try:
            self.db.session.add(entity)
            self.db.session.commit()
            return entity
        except Exception as e:
            self.db.session.rollback()
            raise e

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()