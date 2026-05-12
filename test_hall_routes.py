from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
import pytest
from database import get_session
from main import app
from models_b import Hall, HallType


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
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
    yield client
    app.dependency_overrides.clear()


def _create_hall_type(session: Session, type_name: str = "Standard") -> HallType:
    hall_type = HallType(type_name=type_name)
    session.add(hall_type)
    session.commit()
    session.refresh(hall_type)
    return hall_type


def _create_hall(session: Session, type_id: int) -> Hall:
    hall = Hall(type_id=type_id)
    session.add(hall)
    session.commit()
    session.refresh(hall)
    return hall


def test_get_halls_empty_returns_empty_list(client: TestClient):
    response = client.get("/halls")
    assert response.status_code == 200
    assert response.json() == []


def test_get_halls_returns_created_hall(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "IMAX")
    hall = _create_hall(session, hall_type.id)

    response = client.get("/halls")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == hall.id
    assert data[0]["type_id"] == hall_type.id


def test_get_halls_filter_no_match_returns_empty_list(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "IMAX")
    _create_hall(session, hall_type.id)

    response = client.get("/halls", params={"type_name": "VIP"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_hall_not_found_returns_404(client: TestClient):
    response = client.get("/halls/9999")
    assert response.status_code == 404


def test_get_hall_returns_hall(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")
    hall = _create_hall(session, hall_type.id)

    response = client.get(f"/halls/{hall.id}")
    assert response.status_code == 200
    assert response.json()["id"] == hall.id
    assert response.json()["type_id"] == hall_type.id


def test_get_halls_with_type_name_static_route_not_422(client: TestClient):
    response = client.get("/halls/with-type-name")
    assert response.status_code == 200


def test_get_halls_with_type_name_filter_no_match_returns_empty(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "IMAX")
    _create_hall(session, hall_type.id)

    response = client.get("/halls/with-type-name", params={"type_name": "VIP"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_halls_with_type_name_returns_id_type_id_and_type_name(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "IMAX")
    hall = _create_hall(session, hall_type.id)

    response = client.get("/halls/with-type-name")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == hall.id
    assert data[0]["type_id"] == hall_type.id
    assert data[0]["type_name"] == "IMAX"


def test_get_hall_with_type_name_returns_id_type_id_and_type_name(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "IMAX")
    hall = _create_hall(session, hall_type.id)

    response = client.get(f"/halls/{hall.id}/with-type-name")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == hall.id
    assert data["type_id"] == hall_type.id
    assert data["type_name"] == "IMAX"


def test_get_hall_with_type_name_not_found_returns_404(client: TestClient):
    response = client.get("/halls/9999/with-type-name")
    assert response.status_code == 404


def test_create_hall_with_valid_type_id_returns_201(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")

    response = client.post("/halls", json={"type_id": hall_type.id})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["type_id"] == hall_type.id


def test_create_hall_with_invalid_type_id_returns_404(client: TestClient):
    response = client.post("/halls", json={"type_id": 9999})
    assert response.status_code == 404


def test_create_hall_missing_type_id_returns_422(client: TestClient):
    response = client.post("/halls", json={})
    assert response.status_code == 422


def test_put_hall_not_found_returns_404(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")

    response = client.put("/halls/9999", json={"type_id": hall_type.id})
    assert response.status_code == 404


def test_put_hall_with_valid_type_id_returns_updated_hall(client: TestClient, session: Session):
    original_type = _create_hall_type(session, "Standard")
    new_type = _create_hall_type(session, "IMAX")
    hall = _create_hall(session, original_type.id)

    response = client.put(f"/halls/{hall.id}", json={"type_id": new_type.id})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == hall.id
    assert data["type_id"] == new_type.id


def test_put_hall_with_invalid_type_id_returns_404(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")
    hall = _create_hall(session, hall_type.id)

    response = client.put(f"/halls/{hall.id}", json={"type_id": 9999})
    assert response.status_code == 404


def test_put_hall_missing_type_id_returns_422(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")
    hall = _create_hall(session, hall_type.id)

    response = client.put(f"/halls/{hall.id}", json={})
    assert response.status_code == 422


def test_delete_hall_not_found_returns_404(client: TestClient):
    response = client.delete("/halls/9999")
    assert response.status_code == 404


def test_delete_hall_existing_returns_204(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")
    hall = _create_hall(session, hall_type.id)

    response = client.delete(f"/halls/{hall.id}")
    assert response.status_code == 204


def test_delete_hall_existing_then_get_returns_404(client: TestClient, session: Session):
    hall_type = _create_hall_type(session, "Standard")
    hall = _create_hall(session, hall_type.id)

    delete_response = client.delete(f"/halls/{hall.id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/halls/{hall.id}")
    assert get_response.status_code == 404
