from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from typing import Optional
from database import get_session
from models_b import SeatType, SeatTypeCreate


router = APIRouter(prefix="/seat-types", tags=["Seat Types"])


@router.get("", response_model=list[SeatType])
def get_seat_types(
	name: Optional[str] = Query(default=None, description="Filter by seat type name"),
	session: Session = Depends(get_session)
):
	query = select(SeatType)
	if name is not None:
		query = query.where(SeatType.type_name == name)
	seat_types = session.exec(query).all()
	return seat_types


@router.get("/{seat_type_id}", response_model=SeatType)
def get_seat_type(seat_type_id: int, session: Session = Depends(get_session)):
	seat_type = session.get(SeatType, seat_type_id)
	if not seat_type:
		raise HTTPException(status_code=404, detail="SeatType not found")
	return seat_type

@router.post("", response_model=SeatType, status_code=201)
def create_seat_type(seat_type_in: SeatTypeCreate, session: Session = Depends(get_session)):
    """Create a new SeatType."""
    db_seat_type = SeatType.model_validate(seat_type_in)
    session.add(db_seat_type)
    session.commit()
    session.refresh(db_seat_type)
    return db_seat_type

@router.put("/{seat_type_id}", response_model=SeatType)
def put_seat_type(seat_type_id: int, seat_type_in: SeatTypeCreate, session: Session = Depends(get_session)):
	"""Full replace of SeatType: all fields are required in the body."""
	db_seat_type = session.get(SeatType, seat_type_id)
	if not db_seat_type:
		raise HTTPException(status_code=404, detail="SeatType not found")

	data = seat_type_in.model_dump()
	for key, value in data.items():
		setattr(db_seat_type, key, value)

	session.add(db_seat_type)
	session.commit()
	session.refresh(db_seat_type)
	return db_seat_type

@router.delete("/{seat_type_id}", status_code=204)
def delete_seat_type(seat_type_id: int, session: Session = Depends(get_session)):
	db_seat_type = session.get(SeatType, seat_type_id)
	if not db_seat_type:
		raise HTTPException(status_code=404, detail="SeatType not found")

	session.delete(db_seat_type)
	session.commit()

