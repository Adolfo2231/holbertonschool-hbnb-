import sys
import os



from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def test_imports():
    # Prueba de importación de User
    try:
        usuario = User(first_name="Juan", last_name="Pérez", email="juan@ejemplo.com")
        print("✓ Importación de User exitosa")
    except Exception as e:
        print("✗ Error importando User:", str(e))

    # Prueba de importación de Place 
    try:
        lugar = Place(
            title="Casa de Playa",
            price=100.0,
            latitude=20.123,
            longitude=-87.456,
            owner_id="user123"
        )
        print("✓ Importación de Place exitosa")
    except Exception as e:
        print("✗ Error importando Place:", str(e))

    # Prueba de importación de Amenity
    try:
        amenidad = Amenity(name="WiFi")
        print("✓ Importación de Amenity exitosa")
    except Exception as e:
        print("✗ Error importando Amenity:", str(e))

    # Prueba de importación de Review
    try:
        reseña = Review(
            text="Excelente lugar",
            rating=5,
            user_id="user123",
            place_id="place123"
        )
        print("✓ Importación de Review exitosa")
    except Exception as e:
        print("✗ Error importando Review:", str(e))

if __name__ == "__main__":
    test_imports()


