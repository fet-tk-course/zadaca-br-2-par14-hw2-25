from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
import pytest

from main import app
from database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    try:
        yield client
    finally:
        client.close()
        app.dependency_overrides.clear()


def test_create_user(client: TestClient):
    # Test kreiranja novog korisnika
    response = client.post("/users", json={
        "first_name": "Nejla",
        "last_name": "Kavazovic",
        "email": "nejla@example.com",
        "phone_number": "061123456",
        "loyalty_points": 0,
        "is_active": True
    })
    assert response.status_code == 201
    assert response.json()["first_name"] == "Nejla"
    assert response.json()["id"] is not None


def test_get_users(client: TestClient):
    # Test dohvatanja liste korisnika
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_not_found(client: TestClient):
    # Test 404 kada korisnik ne postoji
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_update_user(client: TestClient):
    # Test potpune zamjene korisnika
    created = client.post("/users", json={
        "first_name": "Ana",
        "last_name": "Anic",
        "email": "ana@example.com",
        "phone_number": "062111222",
        "loyalty_points": 0,
        "is_active": True
    }).json()

    response = client.put(f"/users/{created['id']}", json={
        "first_name": "Ana",
        "last_name": "Anic Updated",
        "email": "ana@example.com",
        "phone_number": "062111222",
        "loyalty_points": 10,
        "is_active": True
    })
    assert response.status_code == 200
    assert response.json()["last_name"] == "Anic Updated"


def test_patch_user(client: TestClient):
    # Test djelimičnog ažuriranja korisnika
    created = client.post("/users", json={
        "first_name": "Marko",
        "last_name": "Markovic",
        "email": "marko@example.com",
        "phone_number": "063333444",
        "loyalty_points": 0,
        "is_active": True
    }).json()

    response = client.patch(f"/users/{created['id']}", json={
        "loyalty_points": 50
    })
    assert response.status_code == 200
    assert response.json()["loyalty_points"] == 50
    assert response.json()["first_name"] == "Marko"


def test_delete_user(client: TestClient):
    # Test brisanja korisnika
    created = client.post("/users", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "064555666",
        "loyalty_points": 0,
        "is_active": True
    }).json()

    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 204

    get = client.get(f"/users/{created['id']}")
    assert get.status_code == 404


def test_filter_users_by_active(client: TestClient):
    # Test filtriranja korisnika po is_active
    client.post("/users", json={"first_name": "Aktivan", "last_name": "Korisnik", "email": "aktivan@example.com", "phone_number": "065111111", "loyalty_points": 0, "is_active": True})
    client.post("/users", json={"first_name": "Neaktivan", "last_name": "Korisnik", "email": "neaktivan@example.com", "phone_number": "065222222", "loyalty_points": 0, "is_active": False})

    response = client.get("/users?is_active=true")
    assert response.status_code == 200
    for user in response.json():
        assert user["is_active"] == True