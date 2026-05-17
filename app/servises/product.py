from sqlalchemy.orm import Session
from app.models.detal import Detal


def get_detals(db:Session, limit:int=100, offset:int=0):
    return db.query(Detal).offset(offset).limit(limit).all()


def get_detal(db:Session, number_of_detal:int):
    return db.query(Detal).filter(Detal.article_number == number_of_detal).first()

