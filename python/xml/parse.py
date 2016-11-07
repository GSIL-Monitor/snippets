# -*- coding: utf-8 -*-
from lxml import etree

tables = []

with open('dataset.xml', 'r') as f:
    doc = etree.fromstring(f.read())
    for t in doc.xpath('//table'):
        print('table name: %s' % t.get('name'))
        table = []
        for r in t.xpath('.//row'):
            print(r)
            row = {}
            for c in r.xpath('.//*'):
                print(c.tag)
                print(c)
                row[c.tag] = c.text
            table.append(row)
        tables.append(table)

print(tables)
