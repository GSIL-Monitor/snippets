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

        rowIds = [row['id'] for row in rows]
        existing = self.queryNew(rowIds)

        for row in rows:
            rowId = row['id']
            self.offset = rowId
            if rowId in existing:
                logger.debug('skipped row {}'.format(rowId))
                continue
            self.copyRow(row)

        logger.info('commit offset to {}'.format(self.offset))
        db.session.commit()

    def query(self, offset):
        sql = """SELECT * FROM did_lppa_v2
        WHERE id > :offset LIMIT :limit
        """
        p = {
            'offset': offset,
            'limit': self.limit,
        }
        rows = db.session.execute(sql, p).fetchall()
        return rows

    def queryNew(self, rowIds):
        if len(rowIds) <= 0:
            return set()
        sql = """SELECT id FROM did_lppa_v3
        WHERE id IN :rowIds"""
        p = {
            'rowIds': rowIds,
        }
        rv = set()
        for row in db.session.execute(sql, p).fetchall():
            rv.add(row['id'])
        return rv

    def copyRow(self, row):
        rowId = row['id']
        blob = row['lppa']

        appList = []
        try:
            lppa = msgpack.unpackb(blob)
            appList = [AppInfo.from_v1(k, v) for k, v in lppa.items()]
        except msgpack.exceptions.UnpackException:
            pass

        return

        if len(appList) <= 0:
            try:
                b = lzma.decompress(blob)
                lppa = simplejson.loads(b)
                appList = [AppInfo(**item) for item in lppa]
            except lzma.LZMAError:
                pass

        if len(appList) <= 0:
            logger.warning('not a valid lppa row {}'.format(rowId))
            return

        lppas = [x.value_v2() for x in appList]
        # pprint.pprint(lppas)

        logger.debug('copying {}'.format(rowId))
        blob = row['lppa']
        o = {
            'v': 3,
            'data': lppas,
        }
        s = simplejson.dumps(o, separators=[':', ','], ensure_ascii=True)
        b = s.encode('ascii')
        blob = zlib.compress(b, 1)
        sql = """INSERT INTO did_lppa_v3 (id, did, lppa)
        VALUES (:rowId, :did, :blob) ON DUPLICATE KEY UPDATE id = id"""
        p = {
            'blob': blob,
            'rowId': row['id'],
            'did': row['did'],
        }
        db.session.execute(sql, p)
        logger.debug('copied {}'.format(rowId))


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
