# -*- coding: utf-8 -*-
import logging
import pprint

from lxml import etree
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

logging.basicConfig(level=logging.DEBUG)

engine = create_engine(
    'mysql+pymysql://root@127.0.0.1/chengpin?charset=utf8', echo=True)
session = sessionmaker(bind=engine,
                       autocommit=True,
                       autoflush=True)()


def generate_insert_sql(table_name, d):
    sql = "INSERT INTO `" + table_name + "` ("

    keys = [x for x in d.keys()]

    sql += ", ".join(map(lambda x: "`" + x + "`", keys)) + ") "
    sql += "VALUES("
    sql += ", ".join(map(lambda x: ":" + x, keys)) + ")"

    logging.debug(sql)

    session.execute(sql, d)

def process_table(table_name, rows):
    for row in rows:
        sql = generate_insert_sql(table_name, row)

tables = []

with open('dataset.xml', 'rb') as f:
    doc = etree.fromstring(f.read())
    for t in doc.xpath('//table'):
        table = {'name': t.get('name'), 'data': []}
        for r in t.xpath('.//row'):
            row = {}
            for c in r.xpath('.//*'):
                row[c.tag] = c.text
            table['data'].append(row)
        tables.append(table)

logging.debug(pprint.pformat(tables))

for t in tables:
    process_table(t['name'], t['data'])
    # session.execute('truncate table `' + t['name'] + '`')
