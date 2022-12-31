from pydantic import BaseModel
from typing import List, Union, Optional

class AdjectiveBase(BaseModel):
    adjective_word: str
    madlib_id: int 

class AdjectiveCreate(AdjectiveBase):
    pass

class Adjective(AdjectiveBase):
    adjective_id: int

    class Config:
        orm_mode = True

class NounBase(BaseModel):
    noun_word: str
    madlib_id: int

class NounCreate(NounBase):
    pass 

class Noun(NounBase):
    noun_id: int

    class Config:
        orm_mode = True

class VerbBase(BaseModel):
    verb_word: str 
    madlib_id: int

class VerbCreate(VerbBase):
    pass 

class Verb(VerbBase):
    verb_id: int

    class Config:
        orm_mode = True

class MiscellanyBase(BaseModel):
    miscellany_word: str
    madlib_id: int 

class MiscellanyCreate(MiscellanyBase):
    pass 

class Miscellany(MiscellanyBase):
    miscellany_id: int

    class Config:
        orm_mode = True

class MadlibBase(BaseModel):
    title: str
    content: str
    active: Optional[bool] = None

class MadlibCreate(MadlibBase):
    pass 

class Madlib(MadlibBase):
    madlib_id: int
    adjectives: List[Adjective]
    nouns: List[Noun]
    verbs: List[Verb]
    miscellanies: List[Miscellany]

    class Config:
        orm_mode = True
