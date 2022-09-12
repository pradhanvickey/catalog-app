from typing import Optional, List, Union

from pydantic import BaseModel, HttpUrl


# Shared properties
class ItemBase(BaseModel):
    title: str
    description: str
    price: float
    is_active: Optional[bool] = True


class ItemCreate(ItemBase):
    encoded_photo: Union[str, bytes]
    extension: str = "png"


class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    encoded_photo: Optional[Union[str, bytes]]
    extension: Optional[str]
    is_active: Optional[bool]


class ItemInDBBase(ItemBase):
    id: Optional[int] = None
    is_active: bool = True
    menu_id: int
    owner_id: int
    image_url: HttpUrl

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties to return to client with multiple data
class ItemMultiple(BaseModel):
    item: List[Item]
    status: str


# Properties to stored in DB
class ItemInDB(ItemInDBBase):
    pass
