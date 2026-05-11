from sqlmodel import SQLModel, Field
from typing import Optional

# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 


class SeatType(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	type_name: str


class SeatTypeCreate(SQLModel):
	type_name: str


class HallType(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	type_name: str


class HallTypeCreate(SQLModel):
	type_name: str


class HallTypeUpdate(SQLModel):
	type_name: Optional[str] = None
