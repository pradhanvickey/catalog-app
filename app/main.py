import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import user, store, menu, items
from app.config import settings

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user.router)
app.include_router(store.router)
app.include_router(menu.router)
app.include_router(items.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
