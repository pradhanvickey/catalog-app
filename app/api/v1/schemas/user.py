from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None,
    is_active: Optional[bool]


class UserInDBBase(UserBase):
    id: Optional[int] = None
    is_active: bool = True

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    access_token: Optional[str]
    token_type: Optional[str]


# Properties to stored in DB
class UserInDB(UserInDBBase):
    pass
