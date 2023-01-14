from fastapi import FastAPI, Path, Query, Form, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Union, Optional
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
import copy
import re

from SQL.database import SessionLocal, engine

from SQL import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory='templates')

def get_DB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

''' 
*CRUD*: RETRIEVE

'''
@app.get('/')
async def root(request: Request, db: Session = Depends(get_DB)):
    titles_n_names = crud.get_madlib_names(db)
    
    return templates.TemplateResponse('landing.html', {
        'request': request,
        'games': dict(titles_n_names)
    })

@app.get('/madlibsgame/{name}')
async def getMadLibGame(request: Request, name: str, 
    db: Session = Depends(get_DB)):
    my_mad_lib = crud.get_madlib_byName(db, name)

    title = my_mad_lib.title
    content = my_mad_lib.content
    display_name = my_mad_lib.display_name

    adjective, noun, verb, miscellany = db.query(models.WordType).filter(models.WordType.word_type_id < 5).all()

    adjectives = [word.word for word in my_mad_lib.words if word.word_type == adjective]
    nouns = [word.word for word in my_mad_lib.words if word.word_type == noun]
    verbs = [word.word for word in my_mad_lib.words if word.word_type == verb]
    miscellanies = [word.word for word in my_mad_lib.words if word.word_type == miscellany]

    return templates.TemplateResponse('madlib.html', {'request': request, 
                                    'display_name': display_name,
                                    'my_mad_lib': content, 
                                    'adjectives': adjectives, 
                                    'nouns': nouns, 
                                    'verbs': verbs, 
                                    'miscellanies': miscellanies})


async def CRUDform(request: Request, name: Union[str, None] = None):
    form_data = request.form()
    form_json = jsonable_encoder(form_data)

    title = form_json["title"] if not name else name
    content = form_json["madlib"]
    display_name = form_json["display_name"] # TODO - Add to CreateRUD.html

    all_words = list()
    for a_key, a_val in form_json.items():
        match = re.search('^(adjective|noun|verb|miscellany)', a_key)
        if match:
            w_type = schemas.PyWordTypeBase(match.group())
            a_word = schemas.PyWordBase(word=a_val, word_type=w_type)
            all_words.append(a_word)

    madlib = schemas.PyMadlibBase(
        title = title,
        content = content,
        display_name = display_name,
        words = all_words
    )
    return madlib

''' 
*CRUD*: CREATE
'''
@app.get('/madlibsform/')
async def form4_C_RUD():
    with open('templates/CreateRUD.html', 'r') as fd:
        CreateRUD_HTML = fd.read()
    return HTMLResponse(CreateRUD_HTML);

@app.post('madlibscreate/{name}')
async def postFormData(db: Session = Depends(get_DB), madlib: schemas.PyMadlibCreate = Depends(CRUDform)):
    crud.add_madlib(db, madlib)
    return RedirectResponse('/madlibsgame/' + madlib.title, status_code=status.HTTP_302_FOUND)

''' 
*CRUD*: UPDATE
'''
@app.get('/madlibschange/{madlib_id}')
async def form4CR_U_D(request: Request, name: str):
    pass

@app.post('/madlibsupdate/{madlib_id}')
async def putFormData(db: Session = Depends(get_DB), madlib: models.Madlib = Depends(CRUDform)):
    pass

''' 
*CRUD*: DELETE
'''
@app.get('/madlibsremove/{madlib_id}')
async def form4CRU_D_(request: Request, name: str):
    pass

@app.delete('/madlibsdelete/{madlib_id}')
async def deleteRecord(name: str, db: Session = Depends(get_DB)):
    pass

'''
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
'''