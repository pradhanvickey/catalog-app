from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.v1 import schemas, crud
from app.dependencies import (get_db, get_current_user, get_user_exception, http_exception)
from app.models import Store, Menu, Item

router = APIRouter(
    tags=["Items"]
)


@router.post("/stores/{store_id}/menus/{menu_id}/items/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Item)
async def create_item(store_id: int,
                      menu_id: int,
                      item_in: schemas.ItemCreate,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    Create new Item
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if user has store and menu with provided store_id and menu_id.
    menu = db.query(Store).join(Menu).filter(Store.owner_id == owner_id).filter(Store.id == store_id).filter(
        Menu.id == menu_id).first()

    if menu is None:
        raise http_exception(status_code=404, detail="Menu not found")
    try:
        menu = crud.item.create_with_menu_owner(db=db, obj_in=item_in, menu_id=menu_id, owner_id=owner_id)
    except IntegrityError:
        raise http_exception(status_code=400, detail="Item already exists")
    return menu


@router.delete("/stores/{store_id}/menus/{menu_id}/items/{item_id}/", status_code=status.HTTP_200_OK,
               response_model=schemas.Item)
async def delete_item(store_id: int,
                      menu_id: int,
                      item_id: int,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    Delete a Item
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if use has store with store_id and menu with menu id that is provided.
    item = db.query(Item).join(Menu).filter(Item.id == item_id).filter(Item.owner_id == owner_id).filter(
        Menu.store_id == store_id).filter(
        Menu.id == menu_id).first()

    if item is None:
        raise http_exception(status_code=404, detail="Item not found")

    item = crud.item.remove(db=db, id=item_id)
    return item


@router.get("/menus/{menu_id}/items/{item_id}/", status_code=status.HTTP_200_OK,
            response_model=schemas.Item)
async def get_item_details(menu_id: int,
                           item_id: int,
                           db: Session = Depends(get_db)):
    """
    Get all item of a store
    """
    # checking if user has store and menu with provided store_id and menu_id.
    item = db.query(Item).filter(Item.menu_id == menu_id).filter(Item.id == item_id).first()
    return item


@router.get("/stores/{unique_store_key}/items/", status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
async def get_item_details(unique_store_key: str,
                           skip: int = 0,
                           limit: int = 10,
                           db: Session = Depends(get_db)):
    """
    Get all items of the store using unique_store_key
    """
    store = db.query(Store).filter(Store.unique_store_key == unique_store_key).first()
    if not store:
        raise http_exception(status_code=404, detail=f"Store not found")

    items = db.query(Item).join(Menu).filter(Menu.store_id == store.id).offset(skip).limit(limit).all()
    return items


@router.put("/stores/{store_id}/menus/{menu_id}/items/{item_id}/", status_code=status.HTTP_200_OK,
            response_model=schemas.Item)
async def update_item(store_id: int,
                      menu_id: int,
                      item_id: int,
                      item_in: schemas.ItemUpdate,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    Update Item
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if use has store with store_id and menu with menu id that is provided.
    item = db.query(Item).join(Menu).filter(Item.id == item_id).filter(Item.owner_id == owner_id).filter(
        Menu.store_id == store_id).filter(
        Menu.id == menu_id).first()

    if item is None:
        raise http_exception(status_code=404, detail="Item not found")

    item = crud.item.get(db=db, id=item_id)
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/stores/{store_id}/menus/{menu_id}/items/", status_code=status.HTTP_200_OK,
            response_model=List[schemas.Item])
async def get_all_item_of_menu(store_id: int,
                               menu_id: int,
                               skip: int = 0,
                               limit: int = 100,
                               current_user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    """
    Get all item of a store using unique_store_key
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")
    store = db.query(Store).filter(Store.id == store_id).filter(Store.owner_id == owner_id).first()
    if store is None:
        raise http_exception(status_code=404, detail="Store not found")

    items = db.query(Item).join(Menu).filter(Menu.store_id == store.id).filter(Item.menu_id == menu_id).offset(
        skip).limit(limit).all()
    return items
