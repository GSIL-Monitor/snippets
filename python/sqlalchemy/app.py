# -*- coding: utf-8 -*-
import json
import logging

from sqlalchemy import create_engine
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData, Table

from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import sessionmaker, scoped_session


logging.basicConfig(
    format='[%(asctime)s %(levelname)-5s %(filename)s:%(lineno)d]\n %(message)s',
    level=logging.WARN
)

logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
logging.debug(logging.getLogger('sqlalchemy.engine').handlers)


# engine = create_engine("mysql+mysqlconnector://root@127.0.0.1:3306/adv")
engine = create_engine("sqlite:///app.db", echo=True)
Base = declarative_base(bind=engine)
logging.debug(Base.metadata)

class JSON(types.TypeDecorator):

    impl = String

    def get_col_spec(self):
        return 'JSON'

    def process_bind_param(self, value, dialect):
        logging.warn(value)
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        logging.warn(value)
        return json.loads(value)

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact = Column(JSON)

Base.metadata.create_all()

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
session = Session()

user = User()

user.contact = {
    'phone': 'xxx',
    'address': 'yyy'
}


# session.add(user)
# session.flush()
# session.commit()

user = session.query(User).first()

logging.debug(user.contact)
