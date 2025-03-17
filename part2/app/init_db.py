from app.extensions import db
from app.models.user import User

def create_default_admin():
    """Crea el usuario admin por defecto si no existe"""
    admin_email = "admin@hbnb.com"
    
    # Verificar si ya existe
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password="Admin2231",  # Se hasheará automáticamente
            first_name="Adolfo",
            last_name="Rodriguez",
            is_admin=True  # Este es el campo importante
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    create_default_admin()