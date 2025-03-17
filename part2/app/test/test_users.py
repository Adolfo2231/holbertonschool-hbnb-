import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/users/"  # Ajusta la URL según sea necesario

def test_create_user_success():
    """✅ Crear un usuario correctamente"""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "ValidPass123"
    }
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_missing_fields():
    """❌ Faltar un campo obligatorio"""
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "password": "ValidPass123"
    }
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert "missing_fields" in response.json()

def test_duplicate_email():
    """❌ Email ya registrado"""
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "john.doe@example.com",  # Email ya registrado
        "password": "ValidPass123"
    }
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert response.json()["error"] == "Email already registered"

def test_invalid_email_format():
    """❌ Email en formato incorrecto"""
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smithexample.com",  # Formato incorrecto
        "password": "ValidPass123"
    }
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid email format"

def test_weak_password():
    """❌ Password no cumple los requisitos"""
    data = {
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob.brown@example.com",
        "password": "1234"  # Demasiado corta
    }
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert "Password" in response.json()["error"]

def test_empty_request():
    """❌ Enviar datos vacíos"""
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 400
    assert "missing_fields" in response.json()

def test_no_request_body():
    """❌ No enviar datos en el body"""
    response = requests.post(BASE_URL)
    assert response.status_code == 400
    assert response.json()["error"] == "No data provided"

def test_invalid_data_types():
    """❌ Enviar un campo con un tipo de dato incorrecto"""
    data = {
        "first_name": 123,  # Debe ser un string
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "ValidPass123"
    }
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert "First name must be a string" in response.json()["error"]

if __name__ == "__main__":
    print("Running API tests...")
    test_create_user_success()
    test_missing_fields()
    test_duplicate_email()
    test_invalid_email_format()
    test_weak_password()
    test_empty_request()
    test_no_request_body()
    test_invalid_data_types()
    print("✅ All tests completed successfully!")
