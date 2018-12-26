# -*- coding: utf-8 -*-
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

e = create_engine('mysql+mysqldb://root@127.0.0.1/test')
s = sessionmaker(bind=e)
ss = s()

rs = ss.execute('SELECT 1').first()
print(rs)
print(type(rs))
print(isinstance(rs, dict))
# print('1')
# rs = ss.execute('UPDATE user SET age = 0')
# print('id: {}'.format(id(rs)))
# rs.close()
#
# print('2')
