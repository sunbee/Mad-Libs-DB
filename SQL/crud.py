from sqlalchemy.orm import Session
from typing import List, Union

from SQL import models, schemas

def get_madlib(db: Session, madlib_id: int):
    return db.query(models.Madlib).filter(models.Madlib.madlib_id == madlib_id).first()

def get_madlib_byTitle(db: Session, madlib_title: str):
    return db.query(models.Madlib).filter(models.Madlib.title == madlib_title).first()

def post_madlib_body(db: Session, madlib: schemas.MadlibCreate):
    db_madlib = models.Madlib(title=madlib.title, content=madlib.content)
    db.add(db_madlib)
    db.commit()    
    db.refresh(db_madlib)
    return db_madlib

def post_madlib_adjectives(db: Session, adjectives: List[schemas.AdjectiveCreate]):
    for adjective in adjectives:
        db_adjective = models.Adjective(**adjective.dict())
        db.add(db_adjective)
    db.commit()
    db_madlib = get_madlib(db, adjectives[0].madlib_id)
    return db_madlib

def post_madlib_nouns(db: Session, nouns: List[schemas.NounCreate]):
    for noun in nouns:
        db_noun = models.Noun(**noun.dict())
        db.add(db_noun)
    db.commit()
    db_madlib = get_madlib(db, nouns[0].madlib_id)
    return db_madlib

def post_madlib_verbs(db: Session, verbs: List[schemas.VerbCreate]):
    for verb in verbs:
        db_verb = models.Verb(**verb.dict())
        db.add(db_verb)
    db.commit()
    db_madlib = get_madlib(db, verbs[0].madlib_id)
    return db_madlib
