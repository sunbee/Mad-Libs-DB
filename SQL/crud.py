from sqlalchemy.orm import Session, exc
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
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.refresh(db_madlib)
        return db_madlib

'''
UPDATE: Modify an existing madlib

'''
def update_mad(db: Session, madlib: schemas.PyMadlibCreate):
    title = madlib.title
    content = madlib.content
    display_name = madlib.display_name
    db_madlib = db.query(models.Madlib).filter(models.Madlib.title==title).one()

    LHS = madlib.getWordList_byType()
    RHS = db_madlib.getWordList_byType()

    left_not_right = list(set(LHS) - set(RHS))  # to add
    right_not_left = list(set(RHS) - set(LHS))  # to remove 

    types_list = db.query(models.WordType.word_type, models.WordType.word_type_id).filter(models.WordType.word_type_id < 5).all()
    types_dict = dict(types_list)

    words2add = list()
    for mad_word in madlib.words:
        if mad_word.word in left_not_right:
            db_word = models.Word(
                            word=mad_word.word, 
                            word_type_id=types_dict.get(mad_word.word_type.word_type), 
                            madlib = db_madlib)
            words2add.append(db_word)

    try:
        db.add_all(words2add)
        db.query(models.Word).filter(models.Word.word.in_(right_not_left), models.Word.madlib == db_madlib).delete(synchronize_session='fetch')
        db.query(models.Madlib).filter(models.Madlib.title == title).update({'content': content, 'display_name': display_name}, synchronize_session='fetch')
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.refresh(db_madlib)
        return db_madlib

'''
DELETE

'''
def del_madlib_byName(db: Session, name: str):
    mid = db.query(models.Madlib.madlib_id).filter(models.Madlib.title==name).one()
    try:
        db.query(models.Word).filter(models.Word.madlib_id==mid).delete(synchronize_session='fetch')
        db.query(models.Madlib).filter(models.Madlib.madlib_id==mid).delete(synchronize_session='fetch')
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    else:
        return mid;
