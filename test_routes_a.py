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


def test_create_genre(client: TestClient):
    # Test kreiranja novog žanra
    response = client.post("/genres", json={
        "name": "Action",
        "description": "Akcioni filmovi",
        "popularity_score": 9.0,
        "movie_count": 0,
        "is_active": True
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Action"


def test_get_genres(client: TestClient):
    # Test dohvatanja liste žanrova
    response = client.get("/genres")
    assert response.status_code == 200


def test_get_genre_not_found(client: TestClient):
    # Test 404 kada žanr ne postoji
    response = client.get("/genres/9999")
    assert response.status_code == 404


def test_create_movie(client: TestClient):
    # Test kreiranja novog filma
    response = client.post("/movies", json={
        "title": "Inception",
        "director": "Christopher Nolan",
        "duration_minutes": 148,
        "release_year": 2010,
        "rating": 8.8,
        "trailer_url": None,
        "is_currently_showing": True,
        "genre_id": None
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Inception"


def test_get_movies(client: TestClient):
    # Test dohvatanja liste filmova
    response = client.get("/movies")
    assert response.status_code == 200


def test_get_movie_not_found(client: TestClient):
    # Test 404 kada film ne postoji
    response = client.get("/movies/9999")
    assert response.status_code == 404