from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import Session, select

from database import create_db_and_tables, engine, get_session
from routes_a import router as router_a
from models_a import Genre, Movie


def seed_data():
    # Popunjavanje baze početnim podacima ako je prazna
    with Session(engine) as session:
        
        # Provjera da li već postoje podaci
        existing = session.exec(select(Genre)).first()
        if existing:
            return

        # Kreiranje žanrova
        action = Genre(name="Action", description="Akcioni filmovi pune adrenalina", popularity_score=9.2, movie_count=3, is_active=True)
        drama = Genre(name="Drama", description="Emotivne i životne priče", popularity_score=8.5, movie_count=2, is_active=True)
        scifi = Genre(name="Sci-Fi", description="Naučna fantastika i futurizam", popularity_score=8.8, movie_count=2, is_active=True)
        crime = Genre(name="Crime", description="Kriminalistički i triler filmovi", popularity_score=9.0, movie_count=2, is_active=True)
        animation = Genre(name="Animation", description="Animirani filmovi za sve uzraste", popularity_score=8.3, movie_count=1, is_active=True)

        session.add_all([action, drama, scifi, crime, animation])
        session.commit()
        session.refresh(action)
        session.refresh(drama)
        session.refresh(scifi)
        session.refresh(crime)
        session.refresh(animation)

        # Kreiranje filmova
        movies = [
            Movie(title="The Dark Knight", director="Christopher Nolan", duration_minutes=152, release_year=2008, rating=9.0, trailer_url="https://www.youtube.com/watch?v=EXeTwQWrcwY", is_currently_showing=False, genre_id=crime.id),
            Movie(title="Inception", director="Christopher Nolan", duration_minutes=148, release_year=2010, rating=8.8, trailer_url="https://www.youtube.com/watch?v=YoHD9XEInc0", is_currently_showing=True, genre_id=scifi.id),
            Movie(title="Interstellar", director="Christopher Nolan", duration_minutes=169, release_year=2014, rating=8.6, trailer_url="https://www.youtube.com/watch?v=zSWdZVtXT7E", is_currently_showing=True, genre_id=scifi.id),
            Movie(title="The Shawshank Redemption", director="Frank Darabont", duration_minutes=142, release_year=1994, rating=9.3, trailer_url="https://www.youtube.com/watch?v=6hB3S9bIaco", is_currently_showing=False, genre_id=drama.id),
            Movie(title="Forrest Gump", director="Robert Zemeckis", duration_minutes=142, release_year=1994, rating=8.8, trailer_url="https://www.youtube.com/watch?v=bLvqoHBptjg", is_currently_showing=False, genre_id=drama.id),
            Movie(title="Mad Max: Fury Road", director="George Miller", duration_minutes=120, release_year=2015, rating=8.1, trailer_url="https://www.youtube.com/watch?v=hEJnMQG9ev8", is_currently_showing=True, genre_id=action.id),
            Movie(title="John Wick", director="Chad Stahelski", duration_minutes=101, release_year=2014, rating=7.4, trailer_url="https://www.youtube.com/watch?v=2AUmvWm5ZDQ", is_currently_showing=True, genre_id=action.id),
            Movie(title="Top Gun: Maverick", director="Joseph Kosinski", duration_minutes=130, release_year=2022, rating=8.3, trailer_url="https://www.youtube.com/watch?v=giXco2jaZ_4", is_currently_showing=True, genre_id=action.id),
            Movie(title="Pulp Fiction", director="Quentin Tarantino", duration_minutes=154, release_year=1994, rating=8.9, trailer_url="https://www.youtube.com/watch?v=s7EdQ4FqbhY", is_currently_showing=False, genre_id=crime.id),
            Movie(title="The Lion King", director="Roger Allers", duration_minutes=88, release_year=1994, rating=8.5, trailer_url="https://www.youtube.com/watch?v=4sj1MT05lAA", is_currently_showing=False, genre_id=animation.id),
        ]

        session.add_all(movies)
        session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kreiranje tabela i punjenje početnim podacima
    if get_session not in app.dependency_overrides:
        create_db_and_tables()
        seed_data()
    yield


app = FastAPI(
    title="Zadaća 2 - REST API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"message": "Zadaća 2 - REST API"}


app.include_router(router_a)
