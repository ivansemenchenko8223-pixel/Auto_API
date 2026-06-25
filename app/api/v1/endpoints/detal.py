from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import config
from app.schemas.detal import DetalData
from app.db.session import get_db
from app.servises.user import get_user_by_username, get_user_by_email
from datetime import timedelta
from app.servises import detal
from app.core.depences import get_current_user
from app.servises.detal import create_detal as create_new_detal, get_detal, get_detals
from app.models.detal import Detal




router = APIRouter(prefix="/detals")


@router.get("/get_all_detal_from_db", tags=["Детали"], summary="Получить все детали из базы данных")
def get_detals(offset:int=0, limit:int=100, db:Session=Depends(get_db)):
    return detal.get_detals(db, limit, offset) 


@router.get("/get_detal_by_article", tags=["Детали"], summary="Получить деталь по артикулу из базы данных")
def get_detal(detal_id:str, db:Session=Depends(get_db)):
    return detal.get_detal(db, detal_id) 


@router.post("/create_new_detal", tags=["Детали"], summary="Добавить деталь в базу данных (Необходимы права админа)")
def create_detal(detal:DetalData, db:Session=Depends(get_db)):
    return create_new_detal(db,detal)