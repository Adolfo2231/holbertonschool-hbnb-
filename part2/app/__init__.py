import os
from flask import Flask
# from flask_restx import Api
from .extensions import db, migrate, bcrypt, jwt
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from .api.v1.admin import api as admin_ns
from .init_db import create_default_admin
from flask_cors import CORS

def create_app(config_class="config.DevelopmentConfig"):
    """
    Flask Application Factory.

    Args:
        config_class (str): Configuration class for Flask app.
        Default is "DevelopmentConfig".

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config_class)

    # Definir ruta absoluta para la base de datos
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(os.path.dirname(basedir), 'hbnb.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar todas las extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Create API instance with Swagger documentation
    api = Api(app, version="1.0", title="HBnB API",
             description="HBnB Application API")

    # Register all namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns)  # Remove path to allow both root and nested routes
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(admin_ns, path='/api/v1/admin')
    
    # Crear tablas y admin por defecto
    with app.app_context():
        # Primero crear todas las tablas
        db.create_all()
        
        try:
            # Luego intentar crear el admin
            create_default_admin()
        except Exception as e:
            print(f"Error creating admin: {e}")
    
    return app