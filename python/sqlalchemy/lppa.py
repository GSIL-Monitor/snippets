# -*- coding: utf-8 -*-
import json
import logging
import lzma
import pprint

# import msgpack
import sqlalchemy
import sqlalchemy.orm

logger = logging.getLogger()

# e = sqlalchemy.create_engine(
#    'mysql+mysqldb://root@127.0.0.1/test?charset=utf8')
e = sqlalchemy.create_engine(
    'mysql+pymysql://pyjob:177B87ab31@rm-bp1q4mtvzei99yj99.mysql.rds.aliyuncs.com/lppa?charset=utf8')
f = sqlalchemy.orm.sessionmaker(bind=e)
s = f()

row = s.execute("""SELECT * FROM did_lppa_v2 WHERE did = :did""", {
    'did': 'a1b3888e5d1f2a0c7da298afe22d8806fb61584b',
}).fetchone()

_ = lzma.decompress(row['lppa'])
_ = json.loads(_)
# pprint.pprint(len(_))
# pprint.pprint(_)

row = s.execute("""SELECT * FROM did_lppa WHERE did = :did""", {
    'did': 'a1b3888e5d1f2a0c7da298afe22d8806fb61584b',
}).fetchone()

_ = lzma.decompress(row['lppa'])
_ = json.loads(_)
pprint.pprint(len(_))
pprint.pprint(_)
