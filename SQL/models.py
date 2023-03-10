from sqlalchemy import Boolean, Integer, String, Column, ForeignKey 
from sqlalchemy.orm import relationship, reconstructor, exc
from typing import Union

from SQL.database import Base

class Madlib(Base):
    __tablename__ = 'madlib'

    madlib_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    display_name = Column(String)

    words = relationship("Word", backref="madlib")

    def getWordList_byType(self, type: Union[str, None] = None):
        if not type:
            return [word.word for word in self.words]
        return [word.word for word in self.words if word.word_type.word_type == type]

class Word(Base):
    __tablename__ = 'word_list'

    word_id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    word_type_id = Column(Integer, ForeignKey("word_type.word_type_id"))
    madlib_id = Column(Integer, ForeignKey("madlib.madlib_id"))

    word_type = relationship("WordType", backref="words")

class WordType(Base):
    __tablename__ = 'word_type'

    word_type_id = Column(Integer, primary_key=True, index=True)
    word_type = Column(String)

