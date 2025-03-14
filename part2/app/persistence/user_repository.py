from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        """Initialize UserRepository with the User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email.

        :param email: Email address of the user.
        :return: User object or None if not found.
        """
        return self.model.query.filter_by(email=email).first()

    def is_email_registered(self, email):
        """
        Check if an email is already registered.

        :param email: Email to check.
        :return: True if email exists, False otherwise.
        """
        return db.session.query(self.model.query.filter_by(email=email).exists()).scalar()
