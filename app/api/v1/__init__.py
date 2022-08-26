from fastapi import APIRouter

from app.api.v1.routers import menu, items, user, store

version_router = APIRouter(prefix="/v1")

version_router.include_router(user.router)
version_router.include_router(store.router)
version_router.include_router(menu.router)
version_router.include_router(items.router)
