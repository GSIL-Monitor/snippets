# -*- coding: utf-8 -*-
import argparse
import logging
import lzma
import sys
import zlib

import magic

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
            'host': 'itunesregister1.mysql.rds.aliyuncs.com',
            'port': 3306,
            'user': 'staff',
            'pwd': '94bXbcvSad',
            'db': 'zhuanqian',
        },
    }
})


class Converter(object):

    def __init__(self, offset, limit):
        self.offset = offset
        self.limit = limit
        self.quit = False
        self.magic = magic.Magic(mime=True)

    def main(self):
        while not self.quit:
            db.reset()
            self.work()
            db.reset()

        logger.info('!!!done!!!')

    def work(self):
        offset = self.offset
        rows = self.query(offset)
        if len(rows) <= 0:
            self.quit = True
            return

        for row in rows:
            self.convert(row)
            self.offset = row['id']

        logger.info('commit offset to {}'.format(self.offset))
        db.session.commit()

    def query(self, offset):
        sql = """SELECT * FROM android_device_subtasks
        WHERE id > :offset LIMIT :limit
        """
        p = {
            'offset': offset,
            'limit': self.limit,
        }
        rows = db.session.execute(sql, p).fetchall()
        return rows

    def convert(self, row):
        blob = row['packages']
        mime = self.magic.from_buffer(blob[:1024])
        if mime != 'application/x-xz':
            return

        blob = lzma.decompress(blob)
        sql = """UPDATE android_device_subtasks
        SET packages = :blob WHERE id = :rowId AND updated_at = :time"""
        p = {
            'blob': blob,
            'rowId': row['id'],
            'time': row['updated_at'],
        }
        db.session.execute(sql, p)
        logger.debug('converted {}'.format(row['id']))


ap = argparse.ArgumentParser()
ap.add_argument('--offset', default=0, type=int)
ap.add_argument('--limit', default=100, type=int)
ap.add_argument('--debug', action='store_true')
options = ap.parse_args()

lvl = logging.INFO
if options.debug:
    lvl = logging.DEBUG

lformat = ('[%(asctime)s %(levelname)s %(name)s:%(lineno)s] %(message)s')
logging.basicConfig(
    level=logging.WARNING,
    format=lformat,
)

logger.handlers.clear()
console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter(lformat))
console.setLevel(lvl)
logger.addHandler(console)
logger.setLevel(lvl)
logger.propagate = False

c = Converter(
    offset=options.offset,
    limit=options.limit,
)

c.main()
