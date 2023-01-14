from pydantic import BaseModel
from typing import List, Union, Optional

class PyWordTypeBase(BaseModel):
    word_type: str

    class Config:
        orm_mode = True

class PyWordTypeCreate(PyWordTypeBase):
    pass

class PyWordType(PyWordTypeBase):
    word_type_id: int

    class Config:
        orm_mode = True

class PyWordBase(BaseModel):
    word: str
    word_type: PyWordTypeBase

    class Config:
        orm_mode = True

class PyWordCreate(PyWordBase):
    pass

class PyWord(PyWordBase):
    word_id: int
    madlib_id: int
    word_type: PyWordType

    class Config:
        orm_mode = True

class PyMadlibBase(BaseModel):
    title: str
    content: str
    display_name: str
    words: List[PyWordBase]

    class Config:
        orm_mode = True

class PyMadlibCreate(PyMadlibBase):
    pass

class PyMadlib(PyMadlibBase):
    madlib_id: int
    words: List[PyWord]
  

    class Config:
        orm_mode = True

