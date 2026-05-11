from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional
from database import get_session
from models_b import HallType, HallTypeCreate, HallTypeUpdate

router = APIRouter(prefix="/hall-types", tags=["Hall Types"])

@router.get("", response_model=list[HallType])
def get_hall_types(
	name: Optional[str] = Query(default=None, description="Filter by hall type name"),
	session: Session = Depends(get_session)
):
	query = select(HallType)
	if name is not None:
		query = query.where(HallType.typeName == name)
	hall_types = session.exec(query).all()
	return hall_types


@router.get("/{hall_type_id}", response_model=HallType)
def get_hall_type(hall_type_id: int, session: Session = Depends(get_session)):
	hall_type = session.get(HallType, hall_type_id)
	if not hall_type:
		raise HTTPException(status_code=404, detail="HallType not found")
	return hall_type


@router.post("", response_model=HallType, status_code=201)
def create_hall_type(hall_type_in: HallTypeCreate, session: Session = Depends(get_session)):
	db_hall_type = HallType.model_validate(hall_type_in)
	session.add(db_hall_type)
	session.commit()
	session.refresh(db_hall_type)
	return db_hall_type


@router.put("/{hall_type_id}", response_model=HallType)
def put_hall_type(hall_type_id: int, hall_type_in: HallTypeCreate, session: Session = Depends(get_session)):
	db_hall_type = session.get(HallType, hall_type_id)
	if not db_hall_type:
		raise HTTPException(status_code=404, detail="HallType not found")

	data = hall_type_in.model_dump()
	for key, value in data.items():
		setattr(db_hall_type, key, value)

	session.add(db_hall_type)
	session.commit()
	session.refresh(db_hall_type)
	return db_hall_type

@router.delete("/{hall_type_id}", status_code=204)
def delete_hall_type(hall_type_id: int, session: Session = Depends(get_session)):
	db_hall_type = session.get(HallType, hall_type_id)
	if not db_hall_type:
		raise HTTPException(status_code=404, detail="HallType not found")

	session.delete(db_hall_type)
	session.commit()