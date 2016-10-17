# -*- coding: utf-8 -*-
import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import Table, Column
from sqlalchemy.types import Integer, String

from sqlalchemy.sql import column, table, select

print(logging.getLogger().handlers)



engine = create_engine('mysql+mysqlconnector://root@127.0.0.1/momoka', echo=True)


Base = declarative_base(bind=engine)


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, default='')


# SessionFactory = sessionmaker(bind=engine)
# Session = scoped_session(SessionFactory)

# session = Session()
# while True:
#     _ = session.query(User).filter_by(id=0).first()
#     print(_)
#     time.sleep(1)

t = User.__table__

connection = engine.connect()
while True:
    engine.execute(select([t.c.id, t.c.name]).where(t.c.id==1)).\
      execution_options(autocommit=False)
    connection.execute('SELECT id, name FROM users WHERE id = 1')
    time.sleep(1)
