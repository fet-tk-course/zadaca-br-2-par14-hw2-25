from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 


class SeatType(SQLModel, table=True):
	__tablename__ = "seat_types"
	id: Optional[int] = Field(default=None, primary_key=True)
	type_name: str
	seats: list["Seat"] = Relationship(back_populates="seat_type")


class SeatTypeCreate(SQLModel):
	type_name: str
	
	@field_validator("type_name")
	@classmethod
	def type_name_must_be_at_least_two_characters_long(cls, value):
		if len(value) < 2:
			raise ValueError("type_name must be at least 2 characters long")
		return value



class HallType(SQLModel, table=True):
	__tablename__ = "hall_types"
	id: Optional[int] = Field(default=None, primary_key=True)
	type_name: str
	halls: list["Hall"] = Relationship(back_populates="hall_type")


class HallTypeCreate(SQLModel):
	type_name: str


class Hall(SQLModel, table=True):
	__tablename__ = "halls"
	id: Optional[int] = Field(default=None, primary_key=True)
	type_id: int = Field(foreign_key="hall_types.id")
	hall_type: Optional[HallType] = Relationship(back_populates="halls")
	seats: list["Seat"] = Relationship(back_populates="hall")


class HallCreate(SQLModel):
	type_id: int



class HallRead(SQLModel):
	id: int
	type_id: int
	type_name: str


class Seat(SQLModel, table=True):
	__tablename__ = "seats"
	id: Optional[int] = Field(default=None, primary_key=True)
	type_id: int = Field(foreign_key="seat_types.id")
	hall_id: int = Field(foreign_key="halls.id")
	seat_type: Optional[SeatType] = Relationship(back_populates="seats")
	hall: Optional[Hall] = Relationship(back_populates="seats")


class SeatCreate(SQLModel):
	type_id: int
	hall_id: int


class SeatUpdate(SQLModel):
	type_id: Optional[int] = None
	hall_id: Optional[int] = None


class Screening(SQLModel, table=True):
	__tablename__ = "screenings"
	id: Optional[int] = Field(default=None, primary_key=True)
	start_time: datetime
	end_time: datetime
	has_break: bool = False
	base_ticket_price: float
	hall_id: int = Field(foreign_key="halls.id")
	movie_id: int = Field(foreign_key="movie.id")


class ScreeningCreate(SQLModel):
	start_time: datetime
	end_time: datetime
	has_break: bool = False
	base_ticket_price: float
	hall_id: int
	movie_id: int

	@field_validator("start_time")
	@classmethod
	def start_time_must_be_in_the_future(cls, value):
		if value < datetime.now():
			raise ValueError("start_time must be in the future")
		return value


class ScreeningUpdate(SQLModel):
	start_time: Optional[datetime] = None
	end_time: Optional[datetime] = None
	has_break: Optional[bool] = None
	base_ticket_price: Optional[float] = None
	hall_id: Optional[int] = None
	movie_id: Optional[int] = None


class ScreeningHallRead(SQLModel):
	id: int
	type_id: int
	type_name: str


class ScreeningMovieRead(SQLModel):
	id: int
	title: str
	director: str
	duration_minutes: int
	release_year: int
	rating: float
	trailer_url: Optional[str] = None
	is_currently_showing: bool
	genre_id: Optional[int] = None


class ScreeningRead(SQLModel):
	id: int
	start_time: datetime
	end_time: datetime
	has_break: bool
	base_ticket_price: float
	hall: ScreeningHallRead
	movie: ScreeningMovieRead

