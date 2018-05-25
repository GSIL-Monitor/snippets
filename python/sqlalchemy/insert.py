# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData, Table


engine = create_engine('mysql+mysqlconnector://root@127.0.0.1/momoka')

meta = MetaData(bind=engine)

t1 = Table('users', meta, autoload=True)

s = t1.insert([t1.c.name]).values({'id': 1, 'name': 'hello'})

rs = engine.execute(s)

if rs.rowcount < 0:
    print(rs)
