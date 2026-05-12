from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    first_name:str
    last_name:str
    email:str
    age:int
    phone_number:str
    is_active:bool=True

class UserCreate(SQLModel):
    first_name:str
    last_name:str
    email:str
    age:int
    phone_number:str

class UserUpdate(SQLModel):
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    email:Optional[str]=None
    age:Optional[int]=None
    phone_number:Optional[str]=None