from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List, Union, Optional

from SQL.database import SessionLocal, engine

from SQL import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_DB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_madlib_body_fromForm(title: str = Form(...), content: str = Form(...)):
    madlib_body = schemas.MadlibBase(title=title, content=content)
    return madlib_body

async def get_madlib_adjectives(id: int, word_list: str = Form(...)):
    madlib_adjectives = [schemas.AdjectiveCreate(adjective_word=word, madlib_id=id) for word in word_list.split(',')]
    return madlib_adjectives

async def get_madlib_nouns(id: int, word_list: str = Form(...)):
    madlib_nouns = [schemas.NounCreate(noun_word=word, madlib_id=id) for word in word_list.split(',')]
    return madlib_nouns

async def get_madlib_verbs(id: int, word_list: str = Form(...)):
    madlib_verbs = [schemas.VerbCreate(verb_word=word, madlib_id=id) for word in word_list.split(',')]
    return madlib_verbs

async def get_madlib_miscellanies(id: int, word_list: str = Form(...)):
    madlib_miscellanies = [schemas.MiscellanyCreate(miscellany_word=word, madlib_id=id) for word in word_list.split(',')]
    return madlib_miscellanies

@app.get('/getmadlib/{id}', response_model=schemas.Madlib)
async def get_madlib_byID(id: int, db: Session = Depends(get_DB)):
    return crud.get_madlib(db, id)

@app.get('/getnamedmadlib/{name}', response_model=schemas.Madlib)
async def get_madlib_byName(name: str, db: Session = Depends(get_DB)):
    return crud.get_madlib_byTitle(db, name)

@app.post('/makemadlibcontent/')
async def make_madlib_content(madlib_body: schemas.MadlibCreate = Depends(get_madlib_body_fromForm), 
    db: Session = Depends(get_DB)):
    db_madlib = crud.get_madlib_byTitle(db, madlib_title=madlib_body.title)
    if db_madlib:
        raise HTTPException(status_code=400, detail="Created no record! Found madlib with title in DB.")
    return crud.post_madlib_body(db, madlib_body)

@app.post('/addmadlib_wordlist/adjective/{id}', response_model=schemas.Madlib)
async def make_madlib_adjectiveList(adjectives: List[schemas.AdjectiveCreate] = Depends(get_madlib_adjectives),
    db: Session = Depends(get_DB)):
    db_madlib = crud.get_madlib(db, adjectives[0].madlib_id)
    if not db_madlib:
        raise HTTPException(status_code=400, detail="Created no record! Found no madlib with that id.")
    else:
        db_adjectives = db_madlib.adjectives
        if db_adjectives:
            raise HTTPException(status_code=400, detail="Added no words! Found adjectives in DB for madlib with id.")
    
    return crud.post_madlib_adjectives(db, adjectives)

@app.post('/addmadlib_wordlist/noun/{id}', response_model=schemas.Madlib)
async def make_madlib_nounList(nouns: List[schemas.NounCreate] = Depends(get_madlib_nouns),
    db: Session = Depends(get_DB)):
    db_madlib = crud.get_madlib(db, nouns[0].madlib_id)
    if not db_madlib:
        raise HTTPException(status_code=400, detail="Created no record! Found no madlib with that id.")
    else:
        db_nouns = db_madlib.nouns
        if db_nouns:
            raise HTTPException(status_code=400, detail="Added no words. Found nouns in DB for madlib with id.")
    
    return crud.post_madlib_nouns(db, nouns)

@app.post('/addmadlib_wordlist/verb/{id}', response_model=schemas.Madlib)
async def make_madlib_verbList(verbs: List[schemas.VerbCreate] = Depends(get_madlib_verbs), 
    db: Session = Depends(get_DB)):
    db_madlib = crud.get_madlib(db, verbs[0].madlib_id)
    if not db_madlib:
        raise HTTPException(status_code=400, detail="Created no record! Found no madlib with that id.")
    else:
        db_verbs = db_madlib.verbs
        if db_verbs:
            raise HTTPException(status_code=400, detail="Added no words. Found verbs in DB for madlib with id.")

    return crud.post_madlib_verbs(db, verbs)

@app.post('/addmadlib_wordlist/miscellany/{id}', response_model=schemas.Madlib)
async def make_madlib_miscellanyList(miscellanies: List[schemas.MiscellanyCreate] = Depends(get_madlib_miscellanies), 
    db: Session = Depends(get_DB)):
    db_madlib = crud.get_madlib(db, miscellanies[0].madlib_id)
    if not db_madlib:
        raise HTTPException(status_code=400, detail="Created no record! Found no madlib with that id.")
    else:
        db_miscellanies = db_madlib.miscellanies
        if db_miscellanies:
            raise HTTPException(status_code=400, detail="Added no words. Found miscellanies in DB for madlib with id.")

    return crud.post_madlib_miscellanies(db, miscellanies)