from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns


def create_app(config_class="config.DevelopmentConfig"):
    """
    Flask Application Factory.

    Args:
        config_class (str): Configuration
        class for Flask app.
        Default is "DevelopmentConfig".

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configuration 

    # Create API instance with Swagger documentation
    api = Api(app, version="1.0", title="HBnB API",
              description="HBnB Application API")

    # Register all namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    return app
