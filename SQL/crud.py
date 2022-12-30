from sqlalchemy.orm import Session

from SQL import models, schemas

def get_madlib(db: Session, madlib_id: int):
    return db.query(models.Madlib).filter(models.Madlib.madlib_id == madlib_id).first()

def get_madlib_byTitle(db: Session, madlib_title: str):
    return db.query(models.Madlib).filter(models.Madlib.title == madlib_title).first()
