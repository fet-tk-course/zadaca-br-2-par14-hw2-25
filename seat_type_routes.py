from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import Optional

from database import get_session
from models_b import SeatType


router = APIRouter(prefix="/seat-types", tags=["Seat Types"])


@router.get("", response_model=list[SeatType])
def get_seat_types(
	name: Optional[str] = Query(default=None, description="Filter po nazivu tipa sjedala"),
	session: Session = Depends(get_session)
):
	query = select(SeatType)
	if name is not None:
		query = query.where(SeatType.typeName == name)
	seat_types = session.exec(query).all()
	return seat_types