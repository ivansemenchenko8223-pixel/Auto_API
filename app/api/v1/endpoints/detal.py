from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.schemas.detal import DetalData
from app.db.session import get_db
from app.core.depences import get_current_admin
from app.servises import detal as detal_service


router = APIRouter(prefix="/detals")


@router.get(
    "/get_all_detal_from_db",
    tags=["Детали"],
    summary="Получить все детали из базы данных",
)
def get_all_detals(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return detal_service.get_detals(db, limit, offset)


@router.get(
    "/get_detal_by_article",
    tags=["Детали"],
    summary="Получить деталь по артикулу из базы данных",
)
def get_detal_by_article(article_number: str, db: Session = Depends(get_db)):
    return detal_service.get_detal(db, article_number)


@router.post(
    "/create_new_detal",
    tags=["Детали"],
    summary="Добавить деталь в базу данных (необходимы права админа)",
)
def create_detal(
    detal: DetalData,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    return detal_service.create_detal(db, detal)
