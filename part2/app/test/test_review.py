from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.services.facade import HBnBFacade

def test_review_creation():
    # Crear el usuario que hará la reseña
    user = User("Ana", "García", "ana@example.com", "password123")
    facade = HBnBFacade()
    facade.create_user(user)

    # Crear el propietario del lugar
    owner = User("Juan", "Pérez", "juan@example.com", "password456") 
    facade.create_user(owner)

    # Crear el lugar que será reseñado
    place = Place(
        title="Apartamento Céntrico",
        description="Hermoso apartamento en el centro",
        price=150,
        latitude=40.4168,
        longitude=-3.7038,
        owner_id=owner
    )
    facade.create_place(place)

    # Crear y probar la reseña usando el facade
    review = Review(text="¡Excelente estancia!", rating=5)
    facade.create_review(review, user, place)

    assert review.text == "¡Excelente estancia!"
    assert review.rating == 5
    assert review.user.first_name == "Ana"
    assert review in place.reviews

# No ejecutes la prueba directamente aquí
# La prueba debe ser ejecutada con un framework como pytest
