# -*- coding: utf-8 -*-
import logging

import msgpack
import sqlalchemy
import sqlalchemy.orm


logger = logging.getLogger()

# e = sqlalchemy.create_engine(
#    'mysql+mysqldb://root@127.0.0.1/test?charset=utf8')
e = sqlalchemy.create_engine(
    'mysql+mysqldb://dbaroot@172.16.3.234/test?charset=utf8')
f = sqlalchemy.orm.sessionmaker(bind=e)
s = f()

p = msgpack.packb(['hello', 'world', 1])
logger.warning(p)

logger.warning(e)

_ = s.execute("""INSERT INTO b(id, b)
VALUES(1, _binary :b)
ON DUPLICATE KEY UPDATE id = 2""", dict(b=p))

logger.warning(s.execute('show warnings').fetchall())

logger.warning(_)
s.commit()
s
