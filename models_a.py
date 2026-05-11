from sqlmodel import SQLModel, Field
from typing import Optional


# ==================== GENRE ====================

class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    popularity_score: float = 0.0
    movie_count: int = 0
    is_active: bool = True


class GenreCreate(SQLModel):
    name: str
    description: Optional[str] = None
    popularity_score: float = 0.0
    is_active: bool = True


class GenreUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    popularity_score: Optional[float] = None
    is_active: Optional[bool] = None


# ==================== MOVIE ====================

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    director: str
    duration_minutes: int
    release_year: int
    rating: float = 0.0
    trailer_url: Optional[str] = None
    is_currently_showing: bool = True
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id")


class MovieCreate(SQLModel):
    title: str
    director: str
    duration_minutes: int
    release_year: int
    rating: float = 0.0
    trailer_url: Optional[str] = None
    is_currently_showing: bool = True
    genre_id: Optional[int] = None


class MovieUpdate(SQLModel):
    title: Optional[str] = None
    director: Optional[str] = None
    duration_minutes: Optional[int] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    trailer_url: Optional[str] = None
    is_currently_showing: Optional[bool] = None
    genre_id: Optional[int] = None
