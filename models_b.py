from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 


class SeatType(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	type_name: str


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


class HallCreate(SQLModel):
	type_id: int



class HallRead(SQLModel):
	id: int
	type_id: int
	type_name: str

