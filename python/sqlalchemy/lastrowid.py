# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

e = create_engine('mysql+pymysql://root@127.0.0.1/test')
s = sessionmaker(bind=e)
ss = s()

# ss.execute('TRUNCATE TABLE user')
# ss.commit()

ss.rollback()

rs = ss.execute('INSERT INTO user VALUES()')
# ss.flush()
rowId = rs.lastrowid
print(rowId)
rs.close()
ss.commit()
