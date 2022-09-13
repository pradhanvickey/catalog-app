from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.v1 import schemas, crud
from app.dependencies import (get_db, get_current_user,
                              get_user_exception, http_exception)
from app.models.menu import Menu
from app.models.store import Store

router = APIRouter(
    tags=["Store"]
)


@router.post("/stores", status_code=status.HTTP_201_CREATED, response_model=schemas.Store)
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
        raise http_exception(status_code=400, detail=f"Store with name {store.name} already exists.")
    return store


@router.get("/stores", status_code=status.HTTP_200_OK, response_model=List[schemas.Store])
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
    return store


@router.get("/stores/{store_id}", response_model=schemas.Store)
async def get_store(store_id: int,
                    current_user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """
    Get store  details of a store using store id.
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id).first()
    if store is None:
        raise http_exception(status_code=404, detail="Store doesn't exists.")
    return store


@router.get("/stores/", response_model=schemas.Store)
async def get_store_using_unique_key(unique_store_key: str,
                                     db: Session = Depends(get_db)):
    """
    Get store details using store id.
    """
    store = db.query(Store).filter(Store.unique_store_key == unique_store_key).first()
    if store is None:
        raise http_exception(status_code=404, detail="Store doesn't exists.")
    return store


@router.get("/stores/{unique_store_key}/menus", response_model=List[schemas.Menu])
async def get_all_menu_of_store(unique_store_key: str,
                                skip: int = 0,
                                limit: int = 100,
                                db: Session = Depends(get_db)):
    """
    Get all menu's of a store using unique_store_key
    """
    store = db.query(Store).filter(Store.unique_store_key == unique_store_key).first()
    if store is None:
        raise http_exception(status_code=404, detail="Store doesn't exists.")
    menus = db.query(Menu).filter(Menu.store_id == store.id).offset(skip).limit(limit).all()
    return menus


@router.patch("/stores/{store_id}", status_code=status.HTTP_200_OK, response_model=schemas.Store)
async def update_store(store_id: int,
                       store_in: schemas.StoreUpdate,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
    Update a store using store id
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id).first()

    if store is None:
        raise http_exception(status_code=404, detail="Store doesn't exists.")

    store = crud.store.update(db=db, db_obj=store, obj_in=store_in)
    return store


@router.delete("/stores/{store_id}", status_code=status.HTTP_200_OK, response_model=schemas.Store)
async def delete_store(store_id: int,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
    Delete a store using store id
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id) \
        .first()

    if store is None:
        raise http_exception(f"Store {store.name} doesn't exists.")

    store = crud.store.remove(db=db, id=store.id)
    return store
