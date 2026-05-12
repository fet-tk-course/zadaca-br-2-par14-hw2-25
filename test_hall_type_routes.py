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
	yield client
	app.dependency_overrides.clear()


def test_create_hall_type(client: TestClient):
	response = client.post("/hall-types", json={"type_name": "Standard Hall"})
	assert response.status_code == 201
	assert response.json()["type_name"] == "Standard Hall"
	assert response.json()["id"] is not None


def test_get_hall_types(client: TestClient):
	client.post("/hall-types", json={"type_name": "Standard Hall"})
	response = client.get("/hall-types")
	assert response.status_code == 200
	assert len(response.json()) == 1


def test_get_hall_types_with_filter(client: TestClient):
	client.post("/hall-types", json={"type_name": "Standard Hall"})
	client.post("/hall-types", json={"type_name": "IMAX Hall"})
	response = client.get("/hall-types", params={"name": "Standard Hall"})
	assert response.status_code == 200
	assert len(response.json()) == 1
	assert response.json()[0]["type_name"] == "Standard Hall"


def test_get_hall_type_not_found(client: TestClient):
	response = client.get("/hall-types/9999")
	assert response.status_code == 404


def test_get_hall_type_by_id(client: TestClient):
	created = client.post("/hall-types", json={"type_name": "Standard Hall"}).json()
	response = client.get(f"/hall-types/{created['id']}")
	assert response.status_code == 200
	assert response.json()["type_name"] == "Standard Hall"
	assert response.json()["id"] == created["id"]


def test_put_hall_type(client: TestClient):
	created = client.post("/hall-types", json={"type_name": "Standard Hall"}).json()
	response = client.put(
		f"/hall-types/{created['id']}",
		json={"type_name": "Premium Hall"}
	)
	assert response.status_code == 200
	assert response.json()["type_name"] == "Premium Hall"
	assert response.json()["id"] == created["id"]


def test_put_hall_type_not_found(client: TestClient):
	response = client.put(
		"/hall-types/9999",
		json={"type_name": "Premium Hall"}
	)
	assert response.status_code == 404


def test_delete_hall_type(client: TestClient):
	created = client.post("/hall-types", json={"type_name": "Standard Hall"}).json()
	response = client.delete(f"/hall-types/{created['id']}")
	assert response.status_code == 204

	get_response = client.get(f"/hall-types/{created['id']}")
	assert get_response.status_code == 404


def test_delete_hall_type_not_found(client: TestClient):
	response = client.delete("/hall-types/9999")
	assert response.status_code == 404
