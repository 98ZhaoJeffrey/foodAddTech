from sqlalchemy.orm import Session
from sqlalchemy import Column, String, UUID
from typing import Union, Any
from jwt_utils import create_refresh_token
from db.Token import Token
from db.User import User

def create_tokens(db: Session, user: User, subject: Union[str, Any]):
    refresh_token = create_refresh_token(subject)
    token_db = Token(user_id=user.id, refresh_token=refresh_token)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return token_db

def get_token(db: Session, user: User) -> Token:
    return db.query(Token).filter(Token.user_id == user.id).first()