from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from database import get_session
from main import app
from models_a import Movie
from models_b import Hall, HallType, Screening


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


def _create_movie(session: Session) -> Movie:
	movie = Movie(
		title="Inception",
		director="Christopher Nolan",
		duration_minutes=148,
		release_year=2010,
		rating=8.8,
		trailer_url=None,
		is_currently_showing=True,
		genre_id=None,
	)
	session.add(movie)
	session.commit()
	session.refresh(movie)
	return movie


def _create_screening(session: Session, hall_id: int, movie_id: int) -> Screening:
	screening = Screening(
		start_time=datetime(2026, 5, 12, 18, 0),
		end_time=datetime(2026, 5, 12, 20, 15),
		has_break=True,
		base_ticket_price=12.5,
		hall_id=hall_id,
		movie_id=movie_id,
	)
	session.add(screening)
	session.commit()
	session.refresh(screening)
	return screening


def test_get_screenings_empty_returns_empty_list(client: TestClient):
	response = client.get("/screenings")
	assert response.status_code == 200
	assert response.json() == []


def test_get_screenings_returns_created_screening(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	screening = _create_screening(session, hall.id, movie.id)

	response = client.get("/screenings")
	assert response.status_code == 200
	data = response.json()
	assert len(data) == 1
	assert data[0]["id"] == screening.id
	assert data[0]["hall_id"] == hall.id
	assert data[0]["movie_id"] == movie.id


def test_get_screenings_with_details_returns_readable_data(client: TestClient, session: Session):
	hall_type = _create_hall_type(session, "IMAX Hall")
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	_create_screening(session, hall.id, movie.id)

	response = client.get("/screenings/with-details")
	assert response.status_code == 200
	data = response.json()
	assert len(data) == 1
	assert data[0]["hall"]["id"] == hall.id
	assert data[0]["hall"]["type_name"] == "IMAX Hall"
	assert data[0]["movie"]["id"] == movie.id
	assert data[0]["movie"]["title"] == "Inception"


def test_get_screening_returns_screening(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	screening = _create_screening(session, hall.id, movie.id)

	response = client.get(f"/screenings/{screening.id}")
	assert response.status_code == 200
	data = response.json()
	assert data["id"] == screening.id
	assert data["hall_id"] == hall.id
	assert data["movie_id"] == movie.id
	assert data["has_break"] is True
	assert data["base_ticket_price"] == 12.5


def test_get_screening_with_details_returns_readable_data(client: TestClient, session: Session):
	hall_type = _create_hall_type(session, "Standard Hall")
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	screening = _create_screening(session, hall.id, movie.id)

	response = client.get(f"/screenings/{screening.id}/with-details")
	assert response.status_code == 200
	data = response.json()
	assert data["id"] == screening.id
	assert data["hall"]["id"] == hall.id
	assert data["hall"]["type_name"] == "Standard Hall"
	assert data["movie"]["id"] == movie.id
	assert data["movie"]["title"] == "Inception"


def test_create_screening_with_valid_ids_returns_201(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)

	response = client.post(
		"/screenings",
		json={
			"start_time": "2026-05-12T18:00:00",
			"end_time": "2026-05-12T20:15:00",
			"has_break": True,
			"base_ticket_price": 12.5,
			"hall_id": hall.id,
			"movie_id": movie.id,
		},
	)
	assert response.status_code == 201
	data = response.json()
	assert data["id"] is not None
	assert data["hall_id"] == hall.id
	assert data["movie_id"] == movie.id
	assert data["has_break"] is True
	assert data["base_ticket_price"] == 12.5


def test_create_screening_overlapping_same_hall_returns_409(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	first_movie = _create_movie(session)
	second_movie = _create_movie(session)

	_create_screening(session, hall.id, first_movie.id)

	response = client.post(
		"/screenings",
		json={
			"start_time": "2026-05-12T19:00:00",
			"end_time": "2026-05-12T21:00:00",
			"has_break": True,
			"base_ticket_price": 12.5,
			"hall_id": hall.id,
			"movie_id": second_movie.id,
		},
	)
	assert response.status_code == 409


def test_put_screening_with_valid_ids_returns_updated_screening(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	first_hall = _create_hall(session, hall_type.id)
	second_hall = _create_hall(session, hall_type.id)
	first_movie = _create_movie(session)
	second_movie = _create_movie(session)
	screening = _create_screening(session, first_hall.id, first_movie.id)

	response = client.put(
		f"/screenings/{screening.id}",
		json={
			"start_time": "2026-05-12T21:00:00",
			"end_time": "2026-05-12T23:00:00",
			"has_break": False,
			"base_ticket_price": 15.0,
			"hall_id": second_hall.id,
			"movie_id": second_movie.id,
		},
	)
	assert response.status_code == 200
	data = response.json()
	assert data["id"] == screening.id
	assert data["hall_id"] == second_hall.id
	assert data["movie_id"] == second_movie.id
	assert data["has_break"] is False
	assert data["base_ticket_price"] == 15.0


def test_patch_screening_updates_only_some_fields(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	first_hall = _create_hall(session, hall_type.id)
	second_hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	screening = _create_screening(session, first_hall.id, movie.id)

	response = client.patch(
		f"/screenings/{screening.id}",
		json={
			"has_break": False,
			"hall_id": second_hall.id,
		},
	)
	assert response.status_code == 200
	data = response.json()
	assert data["id"] == screening.id
	assert data["has_break"] is False
	assert data["hall_id"] == second_hall.id
	assert data["movie_id"] == movie.id
	assert data["base_ticket_price"] == 12.5


def test_delete_screening_existing_returns_204(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	screening = _create_screening(session, hall.id, movie.id)

	response = client.delete(f"/screenings/{screening.id}")
	assert response.status_code == 204


def test_delete_screening_then_get_returns_404(client: TestClient, session: Session):
	hall_type = _create_hall_type(session)
	hall = _create_hall(session, hall_type.id)
	movie = _create_movie(session)
	screening = _create_screening(session, hall.id, movie.id)

	delete_response = client.delete(f"/screenings/{screening.id}")
	assert delete_response.status_code == 204

	get_response = client.get(f"/screenings/{screening.id}")
	assert get_response.status_code == 404
