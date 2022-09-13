from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, HttpUrl


# Shared properties
class StoreBase(BaseModel):
    name: str
    contact_no: str
    address: str


class StoreCreate(StoreBase):
    is_active: Optional[bool] = True
    encoded_photo: Union[str, bytes]
    extension: str = "png"


class StoreUpdate(BaseModel):
    name: Optional[str]
    contact_no: Optional[str]
    address: Optional[str]
    encoded_photo: Optional[Union[str, bytes]]
    extension: Optional[str]
    is_active: Optional[bool]


class StoreInDBBase(StoreBase):
    id: Optional[int] = None
    is_active: bool = True
    owner_id: int
    logo_url: HttpUrl
    qr_code_url: HttpUrl
    unique_store_key: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Store(StoreInDBBase):
    pass


# Properties to return to client with multiple data
class StoreMultiple(BaseModel):
    store: List[Store]


# Properties to stored in DB
class StoreInDB(StoreInDBBase):
    pass
