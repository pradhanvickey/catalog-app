from typing import Optional, List, Union

from pydantic import BaseModel, HttpUrl


# Shared properties
class MenuBase(BaseModel):
    title: str


class MenuCreate(MenuBase):
    is_active: Optional[bool] = True
    encoded_photo: Union[str, bytes]
    extension: str


class MenuUpdate(BaseModel):
    title: Optional[str]
    encoded_photo: Optional[Union[str, bytes]]
    extension: Optional[str]
    is_active: Optional[bool]


class MenuInDBBase(MenuBase):
    id: Optional[int] = None
    is_active: bool = True
    store_id: int
    image_url: HttpUrl

    class Config:
        orm_mode = True


# Properties to return to client
class Menu(MenuInDBBase):
    pass


# Properties to return to client with multiple data
class MenuMultiple(BaseModel):
    menu: List[Menu]

    class Config:
        orm_mode = True


# Properties to stored in DB
class MenuInDB(MenuInDBBase):
    pass
