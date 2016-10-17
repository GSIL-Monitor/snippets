# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData, Table, Column
from sqlalchemy.types import Integer, String

engine = create_engine("mysql+mysqldb://root@localhost/test", echo=True)
session = sessionmaker(bind=engine)
# s = session(autocommit=True, autoflush=True)
s = session(autocommit=False, autoflush=False)
# s.execute("TRUNCATE TABLE user")
# s.commit()

Base = declarative_base(bind=engine)

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))


def commit_or_rollback():
    global s
    try:
        s.commit()
    except Exception as e:
        print(e)
        s.rollback()
    else:
        s.close()

s.execute("INSERT INTO user (username) VALUES ('hello')");
_ = s.execute("SELECT LAST_INSERT_ID()").fetchone();
print(_)
