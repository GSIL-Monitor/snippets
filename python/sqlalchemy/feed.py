# -*- coding: utf-8 -*-
import random
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def randomToken():
    return str(uuid.uuid4()).replace('-', '') * 2


def randomStatus():
    return random.choice([200, 400, 401, 403, 500])


engine = create_engine(
    'mysql+mysqldb://root@127.0.0.1/zhuanqian?charset=utf8')
s = sessionmaker(bind=engine)
ss = s()
ss.execute('SELECT 1')

sql = """INSERT INTO push_result (token, status_code)
VALUES (:token, :code)"""

cnt = 0
for i in range(700000):
    p = {
        'token': randomToken(),
        'code': randomStatus(),
    }
    ss.execute(sql, p)
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt)

ss.commit()
