import os
from datetime import datetime, timedelta
from typing import Union, Any
import jwt
from jwt.exceptions import InvalidTokenError

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 1/2 hour
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(payload, key=JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_JWT(token: str):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, ALGORITHM).get("sub")
    except InvalidTokenError:
        return None