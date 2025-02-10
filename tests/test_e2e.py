import pytest
from flask_jwt_extended import decode_token
from datetime import datetime
from app.models import User
from app.config import current_config
from app.factory import create_app
from app.extensions import db


@pytest.fixture
def app():
    current_config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    current_config.JWT_SECRET_KEY = "some-secret"

    app = create_app(current_config)

    with app.app_context():
        db.create_all()

        connection = db.engine.connect()
        transaction = connection.begin()
        session = db._make_scoped_session(options={"bind": connection, "binds": {}})
        db.session = session

        yield app

        transaction.rollback()
        connection.close()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(app):
    with app.app_context():
        now = datetime.now()
        user = User(
            id=1,
            name="Test User",
            email="test@example.com",
            avatar="https://example.com/avatar.png",
        )

        user.password = user.hash_password("password123")
        user.created_at = now
        user.updated_at = now

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.mark.parametrize("email, password, expected_status, expected_response", [
    ("test@example.com", "password123", 200, {}),
    ("test@example.com", "wrongpassword", 401, {}),
])
def test_login(
    client,
    test_user,
    email,
    password,
    expected_status,
    expected_response
):
    response = client.post("/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == expected_status

    if response.status_code == 200:
        json_data = response.get_json()

        assert "authorization_token" in json_data
        assert "user" in json_data

        token = json_data["authorization_token"]
        decoded_token = decode_token(token)
        assert decoded_token["sub"] == str(test_user.id)

        assert json_data["user"]["email"] == email
        assert json_data["user"]["name"] == test_user.name
        assert json_data["user"]["avatar"] == test_user.avatar

