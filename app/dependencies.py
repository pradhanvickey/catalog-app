from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.db.database import SessionLocal
from app.api.v1.schemas.user import UserInDBBase

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL, scheme_name="JWT")


def generate_access_token(user: UserInDBBase, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode = {"email": user.email, "id": user.id, "exp": expire}
    print(f"{encode=}")
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"{payload=}")
        email: EmailStr = payload.get("email")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise get_user_exception()
        return {"email": email, "id": user_id}
    except JWTError:
        raise get_user_exception()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


# Exception
def http_exception(status_code=404,
                   detail="Store not found"):
    return HTTPException(status_code=status_code, detail=detail)
