import pytest
from app.models import User
from app.config import current_config
from app.factory import create_app
from app.extensions import db


@pytest.fixture
def app():
    """Crea una instancia de la aplicación en modo de prueba."""
    app = create_app(current_config)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Crea un cliente de prueba para enviar requests a la API."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Crea un usuario de prueba en la BD."""
    with app.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
            avatar="https://example.com/avatar.png"
        )
        user.password = user.hash_password("password123")
        db.session.add(user)
        db.session.commit()
        return user


def test_login_success(client, test_user):
    """Prueba un login exitoso."""
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert "authorization_token" in json_data
    assert json_data["user"]["email"] == "test@example.com"


def test_login_invalid_credentials(client, test_user):
    """Prueba el login con credenciales incorrectas."""
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.get_json() == "Invalid Credentials"


def test_login_nonexistent_user(client):
    """Prueba el login con un usuario que no existe."""
    response = client.post("/login", json={
        "email": "fake@example.com",
        "password": "password123"
    })

    assert response.status_code == 401
    assert response.get_json() == "Invalid Credentials"
