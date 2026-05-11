from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    # Tabela za korisnike kino sistema
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str                         # ime korisnika
    last_name: str                          # prezime korisnika
    email: str                              # email adresa
    phone_number: str                       # broj telefona
    loyalty_points: int = 0                 # broj loyalty poena korisnika
    is_active: bool = True                  # da li je korisnički račun aktivan


class UserCreate(SQLModel):
    # Shema za kreiranje novog korisnika
    first_name: str
    last_name: str
    email: str
    phone_number: str
    loyalty_points: int = 0
    is_active: bool = True


class UserUpdate(SQLModel):
    # Shema za djelimično ažuriranje korisnika - sva polja su opcionalna
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    loyalty_points: Optional[int] = None
    is_active: Optional[bool] = None