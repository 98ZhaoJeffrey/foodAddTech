from sqlalchemy.orm import Session

from db.User import User
from db.schemas import UserCreate
from utils.password_utils import hash_password


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, full_name=user.full_name, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, email: str, raw_password: str) -> None:
    db_user = get_user_by_email(db, email)
    db_user.passwords = hash_password(raw_password)
    db.commit()
    db.refresh(db_user)