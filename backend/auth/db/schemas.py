from pydantic import BaseModel
from uuid import UUID
import datetime

class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    hashed_password: str

    class Config:
        orm_mode = True

class TokenBase(BaseModel):
    access_token: str
    refresh_token: str

class Changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenCreate(TokenBase):
    user_id:str
    status:bool
    created_date:datetime.datetime