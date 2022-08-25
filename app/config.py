from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TOKEN_URL: str = "/user/login"
    AWS_ACCESS_KEY: str
    AWS_SECRET: str
    AWS_BUCKET: str
    AWS_REGION: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str = "catalog_app@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "Catalog App"
    BASE_URL: AnyHttpUrl = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()
