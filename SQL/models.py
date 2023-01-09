from sqlalchemy import Boolean, Integer, String, Column, ForeignKey 
from sqlalchemy.orm import relationship

from SQL.database import Base

class Madlib(Base):
    __tablename__ = 'madlib'

    madlib_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    words = relationship("Word", backref="madlib")

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

