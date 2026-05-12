from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional
from database import get_session
from models_b import Hall, HallCreate, HallRead, HallType

router = APIRouter(prefix="/halls", tags=["Halls"])

@router.get("", response_model=list[Hall])
def get_halls(
	type_name: Optional[str] = Query(default=None, description="Filter by hall type name"),
	session: Session = Depends(get_session)
):
	stmt = select(Hall)
	if type_name is not None:
		stmt = stmt.join(HallType).where(HallType.type_name == type_name)
	return session.exec(stmt).all()

@router.get("/with-type-name", response_model=list[HallRead])
def get_halls_with_type_name(
	type_name: Optional[str] = Query(default=None, description="Filter by hall type name"),
	session: Session = Depends(get_session)
):
	stmt = select(Hall.id, Hall.type_id, HallType.type_name).join(HallType)
	if type_name is not None:
		stmt = stmt.where(HallType.type_name == type_name)
	rows = session.exec(stmt).all()
	return [HallRead(id=hall_id, type_id=hall_type_id, type_name=hall_type_name) for hall_id, hall_type_id, hall_type_name in rows]


@router.get("/{hall_id}", response_model=Hall)
def get_hall(hall_id: int, session: Session = Depends(get_session)):
	hall = session.get(Hall, hall_id)
	if not hall:
		raise HTTPException(status_code=404, detail="Hall not found")
	return hall


@router.get("/{hall_id}/with-type-name", response_model=HallRead)
def get_hall_with_type_name(hall_id: int, session: Session = Depends(get_session)):
	stmt = select(Hall.id, Hall.type_id, HallType.type_name).join(HallType).where(Hall.id == hall_id)
	row = session.exec(stmt).first()
	if not row:
		raise HTTPException(status_code=404, detail="Hall not found")
	hall_id_value, hall_type_id, hall_type_name = row
	return HallRead(id=hall_id_value, type_id=hall_type_id, type_name=hall_type_name)


@router.post("", response_model=Hall, status_code=201)
def create_hall(hall_in: HallCreate, session: Session = Depends(get_session)):
	hall_type = session.get(HallType, hall_in.type_id)
	if not hall_type:
		raise HTTPException(status_code=404, detail="HallType not found")

	db_hall = Hall.model_validate(hall_in)
	session.add(db_hall)
	session.commit()
	session.refresh(db_hall)
	return db_hall


@router.put("/{hall_id}", response_model=Hall)
def put_hall(hall_id: int, hall_in: HallCreate, session: Session = Depends(get_session)):
	db_hall = session.get(Hall, hall_id)
	if not db_hall:
		raise HTTPException(status_code=404, detail="Hall not found")

	hall_type = session.get(HallType, hall_in.type_id)
	if not hall_type:
		raise HTTPException(status_code=404, detail="HallType not found")

	data = hall_in.model_dump()
	for key, value in data.items():
		setattr(db_hall, key, value)

	session.add(db_hall)
	session.commit()
	session.refresh(db_hall)
	return db_hall


@router.delete("/{hall_id}", status_code=204)
def delete_hall(hall_id: int, session: Session = Depends(get_session)):
	db_hall = session.get(Hall, hall_id)
	if not db_hall:
		raise HTTPException(status_code=404, detail="Hall not found")

	session.delete(db_hall)
	session.commit()