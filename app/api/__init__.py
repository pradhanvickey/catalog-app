from app.api.v1 import version_router as v1_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)


@api_router.get("/", tags=["base"])
async def get_welcome():
    return "Welcome to this API Demo!"
