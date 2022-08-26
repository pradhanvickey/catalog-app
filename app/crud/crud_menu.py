from typing import List

from sqlalchemy.orm import Session

from app.api.v1 import schemas
from app.crud.base import CRUDBase
from app.models.menu import Menu


class CRUDMenu(CRUDBase[Menu, schemas.MenuCreate, schemas.MenuUpdate]):
    def create_with_shop(self, db: Session, *, obj_in: schemas.StoreCreate, store_id: int) -> Menu:
        url = self.upload_photo_to_s3(obj_in.encoded_photo, obj_in.extension)
        db_obj = Menu(title=obj_in.title,
                      is_active=obj_in.is_active,
                      store_id=store_id,
                      image_url=url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_shop(
            self, db: Session, *, store_id: int, skip: int = 0, limit: int = 100
    ) -> List[Menu]:
        return (
            db.query(self.model)
            .filter(self.model.store_id == store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
            self, db: Session, *, db_obj: Menu, obj_in: schemas.MenuUpdate
    ) -> Menu:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["encoded_photo"] and update_data["extension"]:
            url = self.upload_photo_to_s3(update_data["encoded_photo"], update_data["extension"])
            del update_data["image_url"]
            update_data["image_url"] = url
        return super().update(db, db_obj=db_obj, obj_in=update_data)


menu = CRUDMenu(Menu)
