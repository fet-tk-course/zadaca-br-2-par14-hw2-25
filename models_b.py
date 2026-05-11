from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 


class SeatType(SQLModel, table=True):
	__tablename__ = "seat_types"
	id: Optional[int] = Field(default=None, primary_key=True)
	type_name: str
	seats: list["Seat"] = Relationship(back_populates="seat_type")


class SeatTypeCreate(SQLModel):
	type_name: str


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

