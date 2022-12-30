from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

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

@app.get('/getmadlib/{id}', response_model=schemas.Madlib)
async def get_madlib_byID(id: int, db: Session = Depends(get_DB)):
    return crud.get_madlib(db, id)

@app.get('/getnamedmadlib/{name}', response_model=schemas.Madlib)
async def get_madlib_byName(name: str, db: Session = Depends(get_DB)):
    return crud.get_madlib_byTitle(db, name)





'''

def get_DB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/madlib/{id}', response_model=schemas.Madlib)
async def get_madlib_by_id(id: int, db: Session = Depends(get_DB)):
    madlib = crud.get_madlib(db, id)
    return madlib
'''