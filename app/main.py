from fastapi import FastAPI

from app.core.config import config
from app.api.v1.endpoints.router import router
from app.db.session import engine, Base
from app import models as _models

if not config.SECRET_KEY:
    raise RuntimeError("SECRET_KEY не задан — заполните переменную в .env")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auto API")

app.include_router(router)
