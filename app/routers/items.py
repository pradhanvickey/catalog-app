from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.dependencies import (get_db, get_current_user, get_user_exception, http_exception)
from app.models import Store, Menu, Item

router = APIRouter(
    tags=["Items"]
)


@router.post("/store/{store_id}/menu/{menu_id}/item/", status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
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


@router.delete("/store/{store_id}/menu/{menu_id}/item/{item_id}/", status_code=status.HTTP_201_CREATED,
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

    item = crud.item.remove(db=db, id=id)
    return {"status": f"Item: {item.title} deleted."}


@router.get("/menu/{menu_id}/item/{item_id}/", status_code=status.HTTP_201_CREATED,
            response_model=schemas.Item)
async def get_item_details(menu_id: int,
                           item_id: int,
                           db: Session = Depends(get_db)):
    """
    Get all item of a store
    """
    # checking if user has store and menu with provided store_id and menu_id.
    item = db.query(Item).filter(Item.menu_id == menu_id).filter(Item.id == item_id).first()

    if item is None:
        raise http_exception(status_code=404, detail="item not found")

    return item


@router.put("/store/{store_id}/menu/{menu_id}/item/{item_id}/", status_code=status.HTTP_200_OK,
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


@router.get("/store/{store_id}/menu/{menu_id}/item/", status_code=status.HTTP_201_CREATED,
            response_model=List[schemas.Item])
async def get_all_item_of_menu(store_id: int,
                               menu_id: int,
                               skip: int = 0,
                               limit: int = 100,
                               db: Session = Depends(get_db)):
    """
    Get all item of a store
    """
    # checking if user has store and menu with provided store_id and menu_id.
    menu = db.query(Item).join(Menu).filter(Menu.store_id == store_id).filter(Item.menu_id == menu_id).all()

    if menu is None:
        raise http_exception(status_code=404, detail="Menu not found")
    return menu
