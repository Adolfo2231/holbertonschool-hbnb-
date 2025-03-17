from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.services.facade import HBnBFacade

def test_place_creation():
    # Primero crear y guardar el usuario
    owner = User("John", "Doe", "john@example.com", is_admin=False)
    facade = HBnBFacade()
    facade.user_repo.add(owner)  # Agregar el usuario al repositorio primero
    
    # Luego crear y guardar el lugar
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner_id=owner  # Cambiar 'owner' por 'owner_id'
    )
    facade.place_repo.add(place)  # Agregar el lugar al repositorio

    # Creating and adding a review
    review = Review(
        text="Great stay!", 
        rating=5,
        user_id=owner.id,
        place_id=place.id
    )
    facade.review_repo.add(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert place.owner_id == owner
    print("Place creation and relationship test passed!")

test_place_creation()