from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.dependencies import (get_db, get_current_user, get_user_exception, http_exception)
from app.models import Store, Menu

router = APIRouter(
    tags=["Menu"]
)


@router.post("/store/{store_id}/menu/", status_code=status.HTTP_201_CREATED, response_model=schemas.Menu)
async def create_menu(store_id: int,
                      menu_in: schemas.MenuCreate,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    Create new Menu
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if use has store with store_id provided.
    menu = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id).first()
    if menu is None:
        raise http_exception(status_code=404, detail="Menu not found")
    try:
        menu = crud.menu.create_with_shop(db=db, obj_in=menu_in, store_id=store_id)
    except IntegrityError:
        raise http_exception(status_code=400, detail="Menu already exists")
    return menu


@router.delete("/store/{store_id}/menu/{menu_id}/", status_code=status.HTTP_201_CREATED, response_model=schemas.Menu)
async def delete_menu(store_id: int,
                      menu_id: int,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    Delete a Menu
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if use has store with store_id provided.
    store = db.query(Store).join(Menu).filter(Store.owner_id == owner_id).filter(Store.id == store_id).filter(
        Menu.id == menu_id).first()

    if store is None:
        raise http_exception(status_code=404, detail="Menu not found")

    menu = crud.menu.remove(db=db, id=menu_id)
    return {"status": f"Menu: {menu.title} deleted."}


@router.get("/store/{store_id}/menu", status_code=status.HTTP_201_CREATED, response_model=List[schemas.Menu])
async def get_all_menu(store_id: int,
                       skip: int = 0,
                       limit: int = 100,
                       current_user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    """
    Get all Menu of the store
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if use has store with store_id provided.
    store = db.query(Store).filter(Store.owner_id == owner_id).filter(Store.id == store_id).first()
    if store is None:
        raise http_exception(status_code=404, detail="store not found")

    store = crud.menu.get_multi_by_shop(db=db, store_id=store_id, skip=skip, limit=limit)
    if store is None:
        raise http_exception()
    return store


@router.put("/store/{store_id}/menu/{menu_id}/", status_code=status.HTTP_200_OK, response_model=schemas.Menu)
async def update_menu(store_id: int,
                      menu_id: int,
                      menu_in: schemas.MenuUpdate,
                      current_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """
    Update Menu
    """
    if current_user is None:
        raise get_user_exception()

    owner_id = current_user.get("id")

    # checking if use has menu with store_id and menu_id provided.
    menu = db.query(Store).join(Menu).filter(Store.owner_id == owner_id).filter(Store.id == store_id).filter(
        Menu.id == menu_id).first()

    if menu is None:
        raise http_exception(status_code=404, detail="Menu not found")

    menu = crud.menu.get(db=db, id=menu_id)
    menu = crud.menu.update(db=db, db_obj=menu, obj_in=menu_in)
    return menu
