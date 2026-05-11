from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
import pytest

from main import app
from database import get_session
from models_b import Hall, HallType, Seat, SeatType


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


def _create_seat_type(session: Session, type_name: str = "VIP") -> SeatType:
	seat_type = SeatType(type_name=type_name)
	session.add(seat_type)
	session.commit()
	session.refresh(seat_type)
	return seat_type


def _create_hall_type(session: Session, type_name: str = "Standard Hall") -> HallType:
	hall_type = HallType(type_name=type_name)
	session.add(hall_type)
	session.commit()
	session.refresh(hall_type)
	return hall_type


def _create_hall(session: Session, hall_type_id: int) -> Hall:
	hall = Hall(type_id=hall_type_id)
	session.add(hall)
	session.commit()
	session.refresh(hall)
	return hall


def _create_seat(session: Session, type_id: int, hall_id: int) -> Seat:
	seat = Seat(type_id=type_id, hall_id=hall_id)
	session.add(seat)
	session.commit()
	session.refresh(seat)
	return seat


def test_get_seats_empty_returns_empty_list(client: TestClient):
	response = client.get("/seats")
	assert response.status_code == 200
	assert response.json() == []


def test_get_seats_filter_by_hall_id_no_match_returns_empty_list(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	_create_seat(session, seat_type.id, hall.id)

	other_hall = _create_hall(session, hall_type.id)
	response = client.get("/seats", params={"hall_id": other_hall.id})
	assert response.status_code == 200
	assert response.json() == []


def test_get_seats_filter_by_type_id_no_match_returns_empty_list(client: TestClient, session: Session):
	seat_type = _create_seat_type(session, "VIP")
	other_seat_type = _create_seat_type(session, "Standard")
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	_create_seat(session, seat_type.id, hall.id)

	response = client.get("/seats", params={"type_id": other_seat_type.id})
	assert response.status_code == 200
	assert response.json() == []


def test_get_seats_filter_by_type_name_no_match_returns_empty_list(client: TestClient, session: Session):
	seat_type = _create_seat_type(session, "VIP")
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	_create_seat(session, seat_type.id, hall.id)

	response = client.get("/seats", params={"type_name": "Standard"})
	assert response.status_code == 200
	assert response.json() == []


def test_get_seats_type_id_and_type_name_together_returns_422(client: TestClient):
	response = client.get("/seats", params={"type_id": 1, "type_name": "VIP"})
	assert response.status_code == 422


def test_get_seat_not_found_returns_404(client: TestClient):
	response = client.get("/seats/9999")
	assert response.status_code == 404


def test_create_seat_with_invalid_type_id_returns_404(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)

	response = client.post("/seats", json={"type_id": 9999, "hall_id": hall.id})
	assert response.status_code == 404


def test_create_seat_with_invalid_hall_id_returns_404(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)

	response = client.post("/seats", json={"type_id": seat_type.id, "hall_id": 9999})
	assert response.status_code == 404


def test_create_seat_missing_type_id_returns_422(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)

	response = client.post("/seats", json={"hall_id": hall.id})
	assert response.status_code == 422


def test_create_seat_missing_hall_id_returns_422(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)

	response = client.post("/seats", json={"type_id": seat_type.id})
	assert response.status_code == 422


def test_put_seat_not_found_returns_404(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)

	response = client.put(
		"/seats/9999",
		json={"type_id": seat_type.id, "hall_id": hall.id}
	)
	assert response.status_code == 404


def test_put_seat_with_invalid_type_id_returns_404(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	seat = _create_seat(session, seat_type.id, hall.id)

	response = client.put(
		f"/seats/{seat.id}",
		json={"type_id": 9999, "hall_id": hall.id}
	)
	assert response.status_code == 404


def test_put_seat_with_invalid_hall_id_returns_404(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	seat = _create_seat(session, seat_type.id, hall.id)

	response = client.put(
		f"/seats/{seat.id}",
		json={"type_id": seat_type.id, "hall_id": 9999}
	)
	assert response.status_code == 404


def test_put_seat_missing_type_id_returns_422(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	seat = _create_seat(session, seat_type.id, hall.id)

	response = client.put(f"/seats/{seat.id}", json={"hall_id": hall.id})
	assert response.status_code == 422


def test_put_seat_missing_hall_id_returns_422(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	seat = _create_seat(session, seat_type.id, hall.id)

	response = client.put(f"/seats/{seat.id}", json={"type_id": seat_type.id})
	assert response.status_code == 422


def test_delete_seat_not_found_returns_404(client: TestClient):
	response = client.delete("/seats/9999")
	assert response.status_code == 404


def test_delete_seat_then_get_returns_404(client: TestClient, session: Session):
	seat_type = _create_seat_type(session)
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	seat = _create_seat(session, seat_type.id, hall.id)

	delete_response = client.delete(f"/seats/{seat.id}")
	assert delete_response.status_code == 204

	get_response = client.get(f"/seats/{seat.id}")
	assert get_response.status_code == 404
