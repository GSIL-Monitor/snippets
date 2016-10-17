# -*- coding: utf-8 -*-
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import Column, MetaData
from sqlalchemy.types import Integer, String



logging.basicConfig(level=logging.INFO)

engine = create_engine('sqlite:///test.db')

meta = MetaData(bind=engine)


Base = declarative_base(metadata=meta)

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)

meta.create_all()

SessionFactory = sessionmaker()
SessionFactory.configure(bind=engine, autocommit=False, autoflush=False)

def get_session():
    _ = scoped_session(SessionFactory)
    return _()


s1 = get_session()

user = User()
user.id = 1
user.name = 'test user'

s1.add(user)
s1.flush()

user = s1.query(User).filter_by(id=1).first()

logging.info(user)

s2 = get_session()

user = s2.query(User).filter_by(id=1).first()
logging.info(user)
