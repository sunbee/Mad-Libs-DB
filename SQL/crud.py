from sqlalchemy.orm import Session
from typing import List, Union

from SQL import models, schemas

'''
RETRIEVE: Get a madlib by title


'''
def get_madlib_byName(db: Session, name: str):
    return db.query(models.Madlib).filter(models.Madlib.title==name).one()

def get_madlib_names(db: Session):
    titles = [title[0] for title in db.query(models.Madlib.title).all()]
    names = [name[0] for name in db.query(models.Madlib.display_name).all()]
      
    return list(zip(titles, names))

'''
CREATE: Add a new madlib

'''
def add_madlib(db: Session, madlib: schemas.PyMadlibCreate):
    db_madlib = models.Madlib(
        title = madlib.title,
        content = madlib.content,
        display_name = madlib.display_name
    )

    types_list = db.query(models.WordType.word_type, models.WordType.word_type_id).filter(models.WordType.word_type_id < 5).all()
    types_dict = dict(types_list)

    for mad_word in madlib.words:
        db_word = models.Word(
                        word=mad_word.word, 
                        word_type_id=types_dict.get(mad_word.word_type.word_type), 
                        madlib = db_madlib)
    
    try:
        db.add(db_madlib)
        db.commit()
    except:
        db.rollback()
        raise
    else:
        db.refresh(db_madlib)
        return db_madlib

'''
UPDATE: Modify an existing madlib

'''

'''
DELETE

'''

'''

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

def post_madlib_miscellanies(db: Session, miscellanies: List[schemas.MiscellanyCreate]):
    for miscellany in miscellanies:
        db_miscellany = models.Miscellany(**miscellany.dict())
        db.add(db_miscellany)
    db.commit()
    db_madlib = get_madlib(db, miscellanies[0].madlib_id)
    return db_madlib
'''