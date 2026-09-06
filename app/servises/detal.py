from sqlalchemy.orm import Session

from app.models.detal import Detal
from app.schemas.detal import DetalData


def get_detals(db: Session, limit: int = 100, offset: int = 0):
    return db.query(Detal).offset(offset).limit(limit).all()


def get_detal(db: Session, article_number: str):
    normalized = article_number.replace(" ", "").upper()
    return db.query(Detal).filter(Detal.article_number == normalized).first()


def create_detal(db: Session, detal: DetalData):
    db_detal = Detal(**detal.model_dump())
    db.add(db_detal)
    db.commit()
    db.refresh(db_detal)
    return db_detal
