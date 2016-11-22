# -*- coding: utf-8 -*-
import logging
import os
import pprint
import sys


from dbunit.parser import DbUnitParser
from dbunit.operation import DatabaseOperation

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.DEBUG)


test = os.environ.get('TEST') is not None

engine = None
if test:
    engine = create_engine(
        'mysql+pymysql://dbaroot@172.16.3.234/'
        'chengpin?charset=utf8', echo=True)
else:
    engine = create_engine(
        'mysql+pymysql://root@127.0.0.1/'
        'chengpin?charset=utf8', echo=True)
session = sessionmaker(bind=engine, autocommit=True, autoflush=True)()

parser = DbUnitParser()
with open(sys.argv[1], 'rb') as f:
    dataset = parser.parse(f.read())

logging.debug(pprint.pformat(dataset.data_rows))

op = DatabaseOperation()

if not test:
    op.truncate(session, dataset)
op.insert(session, dataset)
