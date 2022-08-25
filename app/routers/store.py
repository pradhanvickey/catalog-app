from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.dependencies import (get_db, get_current_user, get_user_exception, http_exception)
from app.models.menu import Menu
from app.models.store import Store
from app.utils.s3_util import s3

router = APIRouter(
    tags=["Store"]
)


@router.post("/store/", status_code=status.HTTP_201_CREATED, response_model=schemas.Store)
async def create_store(store_in: schemas.StoreCreate,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
    Create new store
    """

    if current_user is None:
        raise get_user_exception()
    owner_id = current_user.get("id")
    try:
        store = crud.store.create_with_owner(db=db, obj_in=store_in, owner_id=owner_id)
    except IntegrityError:
        raise http_exception(status_code=400, detail="User with this email already exists")
    return store


@router.get("/store/", status_code=status.HTTP_201_CREATED, response_model=List[schemas.Store])
async def get_all_store(skip: int = 0,
                        limit: int = 100,
                        current_user: dict = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """
    Get all stores of a user
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = crud.store.get_multi_by_owner(db=db, owner_id=owner_id, skip=skip, limit=limit)
    if store is None:
        raise http_exception()
    return store


@router.get("/store/{store_id}/", response_model=schemas.Store)
async def get_store(store_id: int,
                    current_user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    Get store of a user
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id).first()
    if store is None:
        raise http_exception()
    return store


@router.get("/store/{store_name}", response_model=List[schemas.Menu])
async def get_store_all_menu(store_name: str,
                             db: Session = Depends(get_db)):
    """
    Get store of a user
    """
    store = db.query(Store).filter(Store.name == store_name).first()
    print(store)
    if store is None:
        raise http_exception()
    menus = db.query(Menu).filter(Menu.store_id == store.id).all()
    return menus


@router.put("/store/{store_id}", status_code=status.HTTP_200_OK, response_model=schemas.Store)
async def update_store(store_id: int,
                       store_in: schemas.StoreUpdate,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
    Update a store
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id).first()

    if store is None:
        raise http_exception()

    store = crud.store.update(db=db, db_obj=store, obj_in=store_in)
    return store


@router.delete("/{store_id}", status_code=status.HTTP_200_OK, response_model=schemas.Store)
async def delete_store(store_id: int,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
    Delete a store
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id) \
        .first()

    if store is None:
        raise http_exception()

    store = crud.store.remove(db=db, id=store.id)
    return {"status": f"Store: {store.name} deleted."}


@router.get("/store/qrcode/{store_name}", status_code=status.HTTP_200_OK)
async def delete_store(store_name: str,
                       db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.name == store_name).first()
    if store is None:
        raise http_exception()
    file = s3.download_photo(store.qr_code_url.split("/")[-1])
    return FileResponse(file, media_type = 'application/octet-stream')
