from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models_c import User, UserCreate, UserUpdate, Reservation, ReservationCreate, ReservationUpdate
from typing import List, Optional

router = APIRouter()

# --- KORISNICI ---
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