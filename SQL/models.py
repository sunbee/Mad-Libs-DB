from sqlalchemy import Boolean, Integer, String, Column, ForeignKey 
from sqlalchemy.orm import relationship

from SQL.database import Base

class Madlib(Base):
    __tablename__ = 'madlib'

    madlib_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    active = Column(Boolean)

    adjectives = relationship("Adjective", back_populates="madlib")
    nouns = relationship("Noun", back_populates="madlib")
    verbs = relationship("Verb", back_populates="madlib")
    miscellanies = relationship("Miscellany", back_populates="madlib")

class Adjective(Base):
    __tablename__ = 'adjective'

    adjective_id = Column(Integer, primary_key=True, index=True)
    adjective_word = Column(String)
    madlib_id = Column(Integer, ForeignKey("madlib.madlib_id"))

    madlib = relationship("Madlib", back_populates="adjectives")

class Noun(Base):
    __tablename__ = 'noun'

    noun_id = Column(Integer, primary_key=True, index=True)
    noun_word = Column(String)
    madlib_id = Column(Integer, ForeignKey("madlib.madlib_id"))

    madlib = relationship("Madlib", back_populates="nouns")

class Verb(Base):
    __tablename__ = 'verb'

    verb_id = Column(Integer, primary_key=True, index=True)
    verb_word = Column(String)
    madlib_id = Column(Integer, ForeignKey("madlib.madlib_id"))

    madlib = relationship("Madlib", back_populates="verbs")

class Miscellany(Base):
    __tablename__ = 'miscellany'

    miscellany_id = Column(Integer, primary_key=True, index=True)
    miscellany_word = Column(String)
    madlib_id = Column(Integer, ForeignKey("madlib.madlib_id"))

    madlib = relationship("Madlib", back_populates="miscellanies")
    