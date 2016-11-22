# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
import logging
import random
import time

from dbunit.helpers import AutoIncrement
from dbunit.generator import Generator
from lxml import etree

# from chengpin import ctx, inject
# from chengpin.boot import CpConfig
# from chengpin.bll.order import OrderService
#
# ctx.register(CpConfig)
# ctx.refresh()
# svc = inject('OrderService', OrderService)

logging.basicConfig(level=logging.DEBUG)

prangers = {
    'id': AutoIncrement(100),
    'shop_id': 0,
    'supplier_id': 0,
    'category_id': 0,
    'warehouse': 0,
    'title': '测试商品',
    'sub_title': '测试副标题',
    'tag': ' ',
    'img': ' ',
    'price': lambda : Decimal(str(random.random() * 100)),
    'delivery_template_id': 0,
    'created_at': lambda : datetime.now(),
    'updated_at': lambda : datetime.now(),
}

srangers = {
    'id': AutoIncrement(),
    'product_id': None,
    'pv': '测试规格',
    'price': lambda : Decimal(str(random.random() * 1000)),
    'stock_total_amount': 100,
    'stock_amount': 100,
    'created_at': lambda : datetime.now(),
    'updated_at': lambda : datetime.now(),
}

pg = Generator(prangers)
sg = Generator(srangers)
products = []
skus = []

for i in range(1, 16):
    p = pg.generate()
    products.append(p.to_xml().decode('UTF-8'))
    s = sg.generate()
    s.product_id = p.id
    skus.append(s.to_xml().decode('UTF-8'))


print('<?xml version="1.0" encoding="UTF-8"?>')
print('<dataset>')
print('<table name="product">')
print('<rows>')
print(''.join(products))
print('</rows>')
print('</table>')
print('<table name="product_sku">')
print('<rows>')
print(''.join(skus))
print('</rows>')
print('</table>')
print('</dataset>')
