from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.api.v1 import schemas
from app.celery_worker import send_email
from app.dependencies import (get_db, generate_access_token, verify_password, get_current_user, http_exception,
                              get_user_exception)
from app.models.user import User

router = APIRouter(
    tags=["User"]
)


def authenticate_user(email: EmailStr, password: str, db):
    """
    Authenticate the user
    """
    user_record = db.query(User).filter(User.email == email).first()
    if not user_record:
        return False
    if not verify_password(password, user_record.hashed_password):
        return False
    return user_record


@router.get("/user/profile/", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_details(current_user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)) -> Any:
    """
    Provide the user info.
    """
    if current_user is None:
        raise get_user_exception()
    user_id = current_user.get("id")
    user_data = crud.user.get(db=db, id=user_id)
    return user_data


@router.post("/user/register/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def register(user_in: schemas.UserCreate,
                   db: Session = Depends(get_db)):
    """
    Register the user.
    """
    try:
        store = crud.user.create(db=db, obj_in=user_in)
        send_email.delay("Registered Successfully", store.email, "Email registration done.")
    except IntegrityError:
        raise http_exception(status_code=400, detail="User with this email already exists")
    return store


@router.post("/user/login/", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    """
    USer login
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    token = generate_access_token(user)
    return {"access_token": token, "token_type": 'Bearer'}


@router.patch("/user/password/reset/", status_code=status.HTTP_200_OK)
async def reset_password(user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Reset Password
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with given email not found")

    crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return {"status": "Password reset completely"}
