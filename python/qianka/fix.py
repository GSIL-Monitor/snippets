# -*- coding: utf-8 -*-
import argparse
import logging
import lzma
import pprint
import sys
import zlib

import magic
import simplejson
import msgpack

from app_info import AppInfo

from qianka.sqlalchemy import QKSQLAlchemy


logger = logging.getLogger(__name__)

db = QKSQLAlchemy()
db.configure({
    'SQLALCHEMY_ECHO': False,
    'SQLALCHEMY_BINDS': {
        'default': {
            'adapter': 'mysql',
            'connector': 'mysqldb',
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'pwd': '',
            'db': 'lppa',
        },
    }
})

db.configure({
    'SQLALCHEMY_ECHO': False,
    'SQLALCHEMY_BINDS': {
        'default': {
            'adapter': 'mysql',
            'connector': 'mysqldb',
            'host': 'rm-bp1q4mtvzei99yj99.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'pyjob',
            'pwd': '177B87ab31',
            'db': 'lppa',
        },
    }
})



sql = """SELECT * FROM dsid_lppa_v2 WHERE id = 3249444"""
row = db.session.execute(sql).fetchone()
blob = row['lppa']
_ = msgpack.unpackb(blob)
pprint.pprint(_)

appList = []
try:
    lppa = msgpack.unpackb(blob)
    appList = [AppInfo.from_v1(k, v) for k, v in lppa.items()]
except msgpack.exceptions.UnpackException:
    pass

pprint.pprint(appList)

#
#  if len(appList) <= 0:
#      try:
#          b = lzma.decompress(blob)
#          lppa = simplejson.loads(b)
#          appList = [AppInfo(**item) for item in lppa]
#      except lzma.LZMAError:
#          pass

# pprint.pprint(appList)
