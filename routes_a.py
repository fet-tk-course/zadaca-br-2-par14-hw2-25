from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import Optional

from database import get_session
from models_a import Genre, GenreCreate, GenreUpdate, Movie, MovieCreate, MovieUpdate


router = APIRouter()


def sync_genre_movie_count(session: Session, genre_id: Optional[int]):
    if genre_id is None:
        return
    genre = session.get(Genre, genre_id)
    if not genre:
        return
    movie_count = session.exec(
        select(func.count(Movie.id)).where(Movie.genre_id == genre_id)
    ).one()
    genre.movie_count = movie_count
    session.add(genre)


@router.get("/genres", response_model=list[Genre])
def get_genres(
    is_active: Optional[bool] = Query(default=None, description="Filter po aktivnosti žanra"),
    session: Session = Depends(get_session)
):
    # Dohvatanje svih žanrova sa opcionalnim filterom po aktivnosti
    query = select(Genre)
    if is_active is not None:
        query = query.where(Genre.is_active == is_active)
    genres = session.exec(query).all()
    return genres


@router.get("/genres/{genre_id}", response_model=Genre)
def get_genre(genre_id: int, session: Session = Depends(get_session)):
    # Dohvatanje jednog žanra po ID-u
    genre = session.get(Genre, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Žanr nije pronađen")
    return genre


@router.post("/genres", response_model=Genre, status_code=201)
def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    # Kreiranje novog žanra
    db_genre = Genre.model_validate(genre)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


@router.put("/genres/{genre_id}", response_model=Genre)
def update_genre(genre_id: int, genre: GenreCreate, session: Session = Depends(get_session)):
    # Potpuna zamjena žanra
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Žanr nije pronađen")
    genre_data = genre.model_dump()
    for key, value in genre_data.items():
        setattr(db_genre, key, value)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


@router.patch("/genres/{genre_id}", response_model=Genre)
def patch_genre(genre_id: int, genre: GenreUpdate, session: Session = Depends(get_session)):
    # Djelimično ažuriranje žanra - ažuriraju se samo poslana polja
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Žanr nije pronađen")
    genre_data = genre.model_dump(exclude_unset=True)
    for key, value in genre_data.items():
        setattr(db_genre, key, value)
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


@router.delete("/genres/{genre_id}", status_code=204)
def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    # Brisanje žanra po ID-u
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Žanr nije pronađen")
    session.delete(db_genre)
    session.commit()




@router.get("/movies", response_model=list[Movie])
def get_movies(
    is_currently_showing: Optional[bool] = Query(default=None, description="Filter po trenutnom prikazivanju"),
    session: Session = Depends(get_session)
):
    # Dohvatanje svih filmova sa opcionalnim filterom po trenutnom prikazivanju
    query = select(Movie)
    if is_currently_showing is not None:
        query = query.where(Movie.is_currently_showing == is_currently_showing)
    movies = session.exec(query).all()
    return movies


@router.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    # Dohvatanje jednog filma po ID-u
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Film nije pronađen")
    return movie


@router.post("/movies", response_model=Movie, status_code=201)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    # Kreiranje novog filma
    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.flush()
    sync_genre_movie_count(session, db_movie.genre_id)
    session.commit()
    session.refresh(db_movie)
    return db_movie


@router.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: MovieCreate, session: Session = Depends(get_session)):
    # Potpuna zamjena filma
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Film nije pronađen")
    old_genre_id = db_movie.genre_id
    movie_data = movie.model_dump()
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    session.add(db_movie)
    if "genre_id" in movie_data and old_genre_id != db_movie.genre_id:
        session.flush()
        sync_genre_movie_count(session, old_genre_id)
        sync_genre_movie_count(session, db_movie.genre_id)
    session.commit()
    session.refresh(db_movie)
    return db_movie


@router.patch("/movies/{movie_id}", response_model=Movie)
def patch_movie(movie_id: int, movie: MovieUpdate, session: Session = Depends(get_session)):
    # Djelimično ažuriranje filma - ažuriraju se samo poslana polja
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Film nije pronađen")
    old_genre_id = db_movie.genre_id
    movie_data = movie.model_dump(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    session.add(db_movie)
    if "genre_id" in movie_data and old_genre_id != db_movie.genre_id:
        session.flush()
        sync_genre_movie_count(session, old_genre_id)
        sync_genre_movie_count(session, db_movie.genre_id)
    session.commit()
    session.refresh(db_movie)
    return db_movie


@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    # Brisanje filma po ID-u
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Film nije pronađen")
    genre_id = db_movie.genre_id
    session.delete(db_movie)
    session.flush()
    sync_genre_movie_count(session, genre_id)
    session.commit()
