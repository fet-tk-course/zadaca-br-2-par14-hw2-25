from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional
from database import get_session
from models_b import Hall, Seat, SeatCreate, SeatType

router = APIRouter(prefix="/seats", tags=["Seats"])

@router.get("", response_model=list[Seat])
def get_seats(
	hall_id: Optional[int] = Query(default=None, description="Filter by hall id"),
	type_id: Optional[int] = Query(default=None, description="Filter by seat type id"),
	type_name: Optional[str] = Query(default=None, description="Filter by seat type name"),
	session: Session = Depends(get_session)
):
	if type_id is not None and type_name is not None:
		raise HTTPException(status_code=422, detail="Send either type_id or type_name, not both")

	stmt = select(Seat)
	if hall_id is not None:
		stmt = stmt.where(Seat.hall_id == hall_id)
	if type_id is not None:
		stmt = stmt.where(Seat.type_id == type_id)
	if type_name is not None:
		stmt = stmt.join(SeatType).where(SeatType.type_name == type_name)

	return session.exec(stmt).all()


@router.get("/{seat_id}", response_model=Seat)
def get_seat(seat_id: int, session: Session = Depends(get_session)):
	seat = session.get(Seat, seat_id)
	if not seat:
		raise HTTPException(status_code=404, detail="Seat not found")
	return seat


@router.post("", response_model=Seat, status_code=201)
def create_seat(seat_in: SeatCreate, session: Session = Depends(get_session)):
	seat_type = session.get(SeatType, seat_in.type_id)
	if not seat_type:
		raise HTTPException(status_code=404, detail="SeatType not found")

	hall = session.get(Hall, seat_in.hall_id)
	if not hall:
		raise HTTPException(status_code=404, detail="Hall not found")

	db_seat = Seat.model_validate(seat_in)
	session.add(db_seat)
	session.commit()
	session.refresh(db_seat)
	return db_seat


@router.put("/{seat_id}", response_model=Seat)
def put_seat(seat_id: int, seat_in: SeatCreate, session: Session = Depends(get_session)):
	db_seat = session.get(Seat, seat_id)
	if not db_seat:
		raise HTTPException(status_code=404, detail="Seat not found")

	seat_type = session.get(SeatType, seat_in.type_id)
	if not seat_type:
		raise HTTPException(status_code=404, detail="SeatType not found")

	hall = session.get(Hall, seat_in.hall_id)
	if not hall:
		raise HTTPException(status_code=404, detail="Hall not found")

	data = seat_in.model_dump()
	for key, value in data.items():
		setattr(db_seat, key, value)

	session.add(db_seat)
	session.commit()
	session.refresh(db_seat)
	return db_seat


@router.delete("/{seat_id}", status_code=204)
def delete_seat(seat_id: int, session: Session = Depends(get_session)):
	db_seat = session.get(Seat, seat_id)
	if not db_seat:
		raise HTTPException(status_code=404, detail="Seat not found")

	session.delete(db_seat)
	session.commit()