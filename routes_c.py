from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models_c import User, UserCreate, UserUpdate, Reservation, ReservationCreate, ReservationUpdate
from typing import List, Optional

router = APIRouter()

@router.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[User])
def get_users(age: Optional[int] = None, session: Session = Depends(get_session)):
    statement = select(User)
    if age:
        statement = statement.where(User.age == age)
    return session.exec(statement).all()

@router.get("/users/{id}", response_model=User)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronadjen")
    return user

@router.patch("/users/{id}", response_model=User)
def update_user(id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronadjen")
    data = user_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/users/{id}", status_code=204)
def delete_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronadjen")
    session.delete(user)
    session.commit()
    return None

@router.post("/reservations", response_model=Reservation, status_code=201)
def create_reservation(res: ReservationCreate, session: Session = Depends(get_session)):
    db_res = Reservation.model_validate(res)
    session.add(db_res)
    session.commit()
    session.refresh(db_res)
    return db_res

@router.get("/reservations", response_model=List[Reservation])
def get_reservations(session: Session = Depends(get_session)):
    return session.exec(select(Reservation)).all()

@router.get("/reservations/{id}", response_model=Reservation)
def get_reservation(id: int, session: Session = Depends(get_session)):
    res = session.get(Reservation, id)
    if not res:
        raise HTTPException(status_code=404, detail="Rezervacija nije pronadjena")
    return res

@router.delete("/reservations/{id}", status_code=204)
def delete_reservation(id: int, session: Session = Depends(get_session)):
    res = session.get(Reservation, id)
    if not res:
        raise HTTPException(status_code=404, detail="Rezervacija nije pronadjena")
    session.delete(res)
    session.commit()
    return None



