# -*- coding: utf-8 -*-
import argparse
import logging
import lzma
import pprint
import sys
import zlib

import magic
import msgpack
import simplejson

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

# db.configure({
#     'SQLALCHEMY_ECHO': False,
#     'SQLALCHEMY_BINDS': {
#         'default': {
#             'adapter': 'mysql',
#             'connector': 'mysqldb',
#             'host': 'rm-bp1q4mtvzei99yj99.mysql.rds.aliyuncs.com',
#             'port': 3306,
#             'user': 'pyjob',
#             'pwd': '177B87ab31',
#             'db': 'lppa',
#         },
#     }
# })


sql = """SELECT * FROM dsid_lppa_v3 WHERE id = 1 LIMIT 1"""
row = db.session.execute(sql).fetchone()
blob = row['lppa']
lppa = msgpack.unpackb(blob)
pprint.pprint(lppa)
