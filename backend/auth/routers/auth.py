import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, Request
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from db.User import User
from db.Token import Token
from db.schemas import UserCreate, TokenBase, Changepassword, UserLogin
from db.database import get_db
from utils.jwt_utils import JWT_SECRET_KEY, decode_JWT, create_access_token
from utils.users_crud import get_user_by_email, create_user, update_password
from utils.tokens_crud import create_JWT, get_token
from utils.password_utils import hash_password
from functools import wraps

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token_blacklist = set() # should change this to a redis instance

def check_expired_token(token: str = Depends()):
    if(token in token_blacklist):
        raise HTTPException(status_code=401, detail="Token is invalid")
    return token

@router.post("/login", response_model=TokenBase)
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hash_password(request.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({
            "id": user.id,
            "username": user.username,
            "name": user.full_name
        })
    token_db = create_JWT(db=db, user=user)
    return {
        "access_token": access_token,
        "refresh_token": token_db
    }

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if(existing_user):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_db = create_user(db, user)
    access_token = create_access_token({
        "id": user.id,
        "username": user.username,
        "name": user.full_name
    })
    token_db = create_JWT(db=db, user=user_db)
    return {
        "access_token": access_token,
        "refresh_token": token_db
    }

@router.post("/token")
def refresh(refresh_token: str):
    try:
        payload = decode_JWT(refresh_token)
        subject = payload.get("sub")
        if subject is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        if refresh_token in token_blacklist:
            raise HTTPException(status_code=401, detail="Refresh token has been revoked")

        new_access_token = create_access_token(payload.get("sub"))
        return {"access_token": new_access_token}
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post('/change-password')
def change_password(request: Changepassword, token: str = Depends(check_expired_token), db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not request.old_password == user.password:
        raise HTTPException(status_code=400, detail="Invalid old password")
    
    update_password(db, request.email, request.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.post("/logout")
def logout(token=Depends(oauth2_scheme)):
    try:
        payload = decode_JWT(token)
        subject = payload.get('sub')
        if subject is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        token_blacklist.add(token)
        return {"message":"Logout Successfully"} 
    except InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")


