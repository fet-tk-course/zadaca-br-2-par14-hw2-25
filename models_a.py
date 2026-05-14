from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator


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

    @field_validator('name')
    @classmethod
    def name_ne_smije_biti_prazan(cls, v):
        if not v.strip():
            raise ValueError('Name ne smije biti prazan string')
        return v.strip()

    @field_validator('popularity_score')
    @classmethod
    def popularity_score_mora_biti_nenegativan(cls, v):
        if v < 0:
            raise ValueError('Popularity score ne smije biti negativan')
        return v


class GenreUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    popularity_score: Optional[float] = None
    is_active: Optional[bool] = None


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
