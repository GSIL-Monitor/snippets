# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql import select

engine = create_engine('mysql+mysqlconnector://root@localhost/qk_action?charset=utf8')

meta = MetaData(bind=engine)

t = Table('a_referer_code', meta, autoload=True)

print(t.c)

s = select([t.c.id, t.c.referer_code])

rs = engine.execute(s)

if rs.rowcount > 0:
    rows = rs.fetchall()

    for row in rows:
        print(row['referer_code'])
