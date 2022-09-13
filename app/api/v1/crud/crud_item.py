from typing import List

from sqlalchemy.orm import Session

from app.api.v1 import schemas
from app.api.v1.crud.base import CRUDBase
from app.models.item import Item
from app.utils.helpers import upload_photo_to_s3


class CRUDItem(CRUDBase[Item, schemas.ItemCreate, schemas.ItemUpdate]):
    def create_with_menu_owner(self, db: Session, *, obj_in: schemas.ItemCreate, menu_id: int, owner_id: int) -> Item:
        url = upload_photo_to_s3(obj_in.encoded_photo, obj_in.extension)
        db_obj = Item(title=obj_in.title.capitalize(),
                      description=obj_in.description,
                      price=obj_in.price,
                      is_active=obj_in.is_active,
                      menu_id=menu_id,
                      owner_id=owner_id,
                      image_url=url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_menu(
            self, db: Session, *, menu_id: int, owner_id:int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(self.model)
            .filter(self.model.menu_id == menu_id)
            .filter(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
            self, db: Session, *, db_obj: Item, obj_in: schemas.ItemUpdate
    ) -> Item:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "encoded_photo" in update_data and  update_data["encoded_photo"] and update_data["extension"]:
            url = upload_photo_to_s3(update_data["encoded_photo"], update_data["extension"])
            del update_data["image_url"]
            update_data["image_url"] = url
        return super().update(db, db_obj=db_obj, obj_in=update_data)


item = CRUDItem(Item)
