from fastapi import FastAPI, Path, Query, Form, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Union, Optional
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session, exc
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

async def CRUDform(request: Request, name: Union[str, None] = None):
    form_data = await request.form()
    form_json = jsonable_encoder(form_data)

    title = form_json["title"] if not name else name
    content = form_json["madlib"]
    display_name = form_json["display_name"] # TODO - Add to CreateRUD.html

    all_words = list()
    for a_key, a_val in form_json.items():
        match = re.search('^(adjective|noun|verb|miscellany)', a_key)
        if match:
            print("Got match: {}".format(match.group()))
            w_type = schemas.PyWordTypeBase(word_type=match.group())
            a_word = schemas.PyWordBase(word=a_val, word_type=w_type)
            all_words.append(a_word)

    try:
        madlib = schemas.PyMadlibBase(
            title = title,
            content = content,
            display_name = display_name,
            words = all_words
        )
        yield madlib
    except Exception as e:
        if isinstance(e, ValueError):
            print(e.args[0])
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unprocessabile entity in form for {}! Gory detail: {}".format(title, str(e)))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Processed no input!")

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
    try:
        my_mad_lib = crud.get_madlib_byName(db, name)
    except Exception as e:
        if isinstance(e, exc.NoResultFound):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Found no madblib by name of {}! Gory detail: {}'.format(name, str(e)))
        elif isinstance(e, exc.SQLAlchemyError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='DB error retrieving {}! Gory detail: {}'.format(name, str(e)))
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Retrieved no madlib!")

    return templates.TemplateResponse('madlib.html', {'request': request, 
                                    'display_name': my_mad_lib.display_name,
                                    'my_mad_lib': my_mad_lib.content, 
                                    'adjectives': my_mad_lib.getWordList_byType('adjective'), 
                                    'nouns': my_mad_lib.getWordList_byType('noun'), 
                                    'verbs': my_mad_lib.getWordList_byType('verb'), 
                                    'miscellanies': my_mad_lib.getWordList_byType('miscellany')})

''' 
*CRUD*: CREATE
'''
@app.get('/madlibsform/')
async def form4_C_RUD():
    with open('templates/CreateRUD.html', 'r') as fd:
        CreateRUD_HTML = fd.read()
    return HTMLResponse(CreateRUD_HTML);

@app.post('/madlibscreate/')
async def postFormData(db: Session = Depends(get_DB), madlib: schemas.PyMadlibCreate = Depends(CRUDform)):
    try:
        crud.add_madlib(db, madlib)
    except Exception as e:
        if isinstance(e, exc.SQLAlchemyError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='DB error creating {}! Gory detail: {}'.format(madlib.title, str(e)))
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Created no madlib!")
    else:
        return RedirectResponse('/madlibsgame/' + madlib.title, status_code=status.HTTP_302_FOUND)

''' 
*CRUD*: UPDATE
'''
@app.get('/madlibschange/{name}')
async def form4CR_U_D(request: Request, name: str, db: Session = Depends(get_DB)):
    try:
        my_mad_lib = crud.get_madlib_byName(db, name)
    except Exception as e:
        if isinstance(e, exc.NoResultFound):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Found no madblib by name of {}! Gory detail: {}'.format(name, str(e)))
        elif isinstance(e, exc.SQLAlchemyError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='DB error retrieving {} to update! Gory detail: {}'.format(name, str(e)))
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Retrieved no madlib for update!")

    return templates.TemplateResponse('CRUpdateD.html', {'request': request, 
                                    'title': my_mad_lib.title,
                                    'display_name': my_mad_lib.display_name,
                                    'HTML': my_mad_lib.content, 
                                    'adjectives': my_mad_lib.getWordList_byType('adjective'), 
                                    'nouns': my_mad_lib.getWordList_byType('noun'), 
                                    'verbs': my_mad_lib.getWordList_byType('verb'), 
                                    'miscellanies': my_mad_lib.getWordList_byType('miscellany')})


@app.post('/madlibsupdate/{name}')
async def putFormData(db: Session = Depends(get_DB), madlib: models.Madlib = Depends(CRUDform)):
    try:
        my_mad_lib = crud.update_mad(db, madlib)
    except Exception as e:
        if isinstance(e, exc.SQLAlchemyError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='DB error updating {}! Gory detail: {}'.format(madlib.title, str(e)))
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Updated no madlib!")
    else:
        return RedirectResponse('/madlibsgame/' + madlib.title, status_code=status.HTTP_302_FOUND)

''' 
*CRUD*: DELETE
'''
@app.get('/madlibsremove/{name}')
async def form4CRU_D_(request: Request, name: str,
    db: Session = Depends(get_DB)):
    try:
        my_mad_lib = crud.get_madlib_byName(db, name)
    except Exception as e:
        if isinstance(e, exc.NoResultFound):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Found no madblib by name of {}! Gory detail: {}'.format(name, str(e)))
        elif isinstance(e, exc.SQLAlchemyError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='DB error retrieving {} to delete! Gory detail: {}'.format(name, str(e)))
        else: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Retrieved no madlib for deletion!")

    return templates.TemplateResponse('CRUDelete.html', {'request': request, 
                                    'title': my_mad_lib.title,
                                    'display_name': my_mad_lib.display_name,
                                    'HTML': my_mad_lib.content, 
                                    'adjectives': my_mad_lib.getWordList_byType('adjective'), 
                                    'nouns': my_mad_lib.getWordList_byType('noun'), 
                                    'verbs': my_mad_lib.getWordList_byType('verb'), 
                                    'miscellanies': my_mad_lib.getWordList_byType('miscellany')})

@app.post('/madlibsdelete/{name}')
async def deleteRecord(name: str, db: Session = Depends(get_DB)):
    try:
        mid = crud.del_madlib_byName(db, name)
    except Exception as e:
        if isinstance(e, exc.NoResultFound):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Found no madblib by name of {} - already deleted?! Gory detail: {}'.format(name, str(e)))
        elif isinstance(e, exc.SQLAlchemyError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='DB error deleting {}! Gory detail:{}'.format(name, str(e)))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Deleted no madlib!')
    else:
        return mid
