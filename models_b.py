from sqlmodel import SQLModel, Field
from typing import Optional

# TODO: Student B - Definiši svoj SQLModel entitet ovdje
# 


class SeatType(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	typeName: str


class SeatTypeCreate(SQLModel):
	typeName: str


class SeatTypeUpdate(SQLModel):
	typeName: Optional[str] = None
