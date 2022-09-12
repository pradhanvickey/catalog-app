from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from app.api.v1 import schemas
from app.api.v1.crud.base import CRUDBase
from app.models.store import Store
from app.utils.helpers import upload_photo_to_s3, create_qr_code_url


class CRUDStore(CRUDBase[Store, schemas.StoreCreate, schemas.StoreUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: schemas.StoreCreate, owner_id: int) -> Store:
        logo_url = upload_photo_to_s3(obj_in.encoded_photo, obj_in.extension)
        unique_store_key = str(uuid4())
        qr_code_url = create_qr_code_url(unique_store_key)

        db_obj = Store(name=obj_in.name,
                       contact_no=obj_in.contact_no,
                       address=obj_in.address,
                       is_active=obj_in.is_active,
                       owner_id=owner_id,
                       logo_url=logo_url,
                       qr_code_url=qr_code_url,
                       unique_store_key=unique_store_key)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Store]:
        return (
            db.query(self.model)
            .filter(Store.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
            self, db: Session, *, db_obj: Store, obj_in: schemas.StoreUpdate
    ) -> Store:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "encoded_photo" in update_data and update_data["encoded_photo"] and update_data["extension"]:
            url = upload_photo_to_s3(update_data["encoded_photo"], update_data["extension"])
            del update_data["logo_url"]
            update_data["logo_url"] = url
        return super().update(db, db_obj=db_obj, obj_in=update_data)


store = CRUDStore(Store)
