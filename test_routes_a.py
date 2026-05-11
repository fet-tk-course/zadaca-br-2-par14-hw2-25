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
    assert response.json()["movie_count"] == 0


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


def test_movie_count_updates_on_movie_create_and_delete(client: TestClient):
    genre = client.post("/genres", json={
        "name": "Drama",
        "description": "Drama filmovi",
        "popularity_score": 8.0,
        "is_active": True
    }).json()

    create_movie_response = client.post("/movies", json={
        "title": "Test Movie",
        "director": "Test Director",
        "duration_minutes": 120,
        "release_year": 2020,
        "rating": 7.5,
        "is_currently_showing": True,
        "genre_id": genre["id"]
    })
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    genre_after_create = client.get(f"/genres/{genre['id']}").json()
    assert genre_after_create["movie_count"] == 1

    delete_movie_response = client.delete(f"/movies/{movie_id}")
    assert delete_movie_response.status_code == 204

    genre_after_delete = client.get(f"/genres/{genre['id']}").json()
    assert genre_after_delete["movie_count"] == 0


def test_movie_count_updates_when_movie_changes_genre(client: TestClient):
    old_genre = client.post("/genres", json={
        "name": "Old Genre",
        "description": "Old",
        "popularity_score": 7.0,
        "is_active": True
    }).json()
    new_genre = client.post("/genres", json={
        "name": "New Genre",
        "description": "New",
        "popularity_score": 9.0,
        "is_active": True
    }).json()

    create_movie_response = client.post("/movies", json={
        "title": "Reassign Movie",
        "director": "Test Director",
        "duration_minutes": 100,
        "release_year": 2021,
        "rating": 8.0,
        "is_currently_showing": True,
        "genre_id": old_genre["id"]
    })
    movie_id = create_movie_response.json()["id"]

    patch_movie_response = client.patch(f"/movies/{movie_id}", json={
        "genre_id": new_genre["id"]
    })
    assert patch_movie_response.status_code == 200

    old_genre_after_patch = client.get(f"/genres/{old_genre['id']}").json()
    new_genre_after_patch = client.get(f"/genres/{new_genre['id']}").json()
    assert old_genre_after_patch["movie_count"] == 0
    assert new_genre_after_patch["movie_count"] == 1
