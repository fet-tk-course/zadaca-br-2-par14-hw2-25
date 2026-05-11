from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional

from database import get_session
from models_users import User, UserCreate, UserUpdate


router = APIRouter()


@router.get("/users", response_model=list[User])
def get_users(
    is_active: Optional[bool] = Query(default=None, description="Filter po aktivnosti korisnika"),
    session: Session = Depends(get_session)
):
    # Dohvatanje svih korisnika sa opcionalnim filterom po aktivnosti
    query = select(User)
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    users = session.exec(query).all()
    return users


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    # Dohvatanje jednog korisnika po ID-u
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    return user


@router.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Kreiranje novog korisnika
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, session: Session = Depends(get_session)):
    # Potpuna zamjena korisnika
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    user_data = user.model_dump()
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/users/{user_id}", response_model=User)
def patch_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    # Djelimično ažuriranje korisnika - ažuriraju se samo poslana polja
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    # Brisanje korisnika po ID-u
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    session.delete(db_user)
    session.commit()