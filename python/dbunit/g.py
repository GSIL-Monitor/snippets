# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
import logging
import random
import time

from dbunit.generator import Generator
from lxml import etree

from chengpin import ctx, inject
from chengpin.boot import CpConfig
from chengpin.bll.order import OrderService

ctx.register(CpConfig)
ctx.refresh()
svc = inject('OrderService', OrderService)

logging.basicConfig(level=logging.DEBUG)

order_ids = set()
user_id = 3326133

detail_id = 1000000
def get_detail_id():
    global detail_id
    detail_id += 1
    return detail_id

address_id = 100000
def get_address_id():
    global address_id
    address_id += 1
    return address_id

def to_xml(_):
    row = etree.Element('row')
    for c in _.__columns__:
        cld = etree.SubElement(row, c)
        v = getattr(_, c)
        if type(v) == Decimal:
            v = '%.2f' % v
        if type(v) == datetime:
            v = v.strftime('%Y-%m-%d %H:%M:%S')
        cld.text = str(v)

    return etree.tostring(row, pretty_print=True)

orangers = {
    'id': None,
    'preprocess_state': list((0, 100, 200, 200, 200, 200, 200)),
    'payment_state': list((0,)),
    'order_state': list((0,)),
    'user_id': user_id, #range(1, 1000000),
    'is_hidden': list((1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    'subtotal_price': lambda : Decimal(random.random() * 100),
    'grand_total_price': lambda : Decimal(random.random() * 1000 + 1000),
    'shipping_cost': lambda : Decimal(random.random() * 200),
    'note': '备注信息',
    'ordered_datetime': lambda: datetime.now(),
    'paid_datetime': lambda: datetime.now(),
    'shipping_datetime': lambda: datetime.now(),
    'completed_datetime': lambda: datetime.now(),
    'created_at': lambda: datetime.now(),
    'updated_at': lambda: datetime.now(),
}

odrangers = {
    'id': lambda : get_detail_id(),
    'order_id': None,
    'product_id': lambda : int(random.random() * 1000000),
    'sku_id': lambda : int(random.random() * 10000),
    'snapshot_key': 'c4ca4238a0b923820dcc509a6f75849b',
    'unit_price': lambda : Decimal(random.random() * 100 + 50),
    'real_unit_price': lambda: Decimal(random.random() * 50),
    'quantity': lambda : int(random.random() * 10),
    'created_at': lambda: datetime.now(),
    'updated_at': lambda: datetime.now(),
}

asrangers = {
    'id': None,
    'aftersales_type': None,
    'aftersales_state': list((10, 20)),
    'user_id': user_id,
    'order_id': None,
    'product_id': None,
    'sku_id': None,
    'snapshot_key': None,
    'note': '描述',
    'refund_amount': 0,
    'quantity': 0,
    'payment_no': '',
}

oarangers = {
    'id': lambda : get_address_id(),
    'area_id': range(3650),
    'city_id': range(390),
    'province_id': range(36),
    'order_id': None,
    'shipto_name': list(('张三', '李四', '王五', '赵六')),
    'contact_name': list(('张三', '李四', '王五', '赵六')),
    'phone': 13812345678,
    'address1': '这是一个测试用的地址嗯',
    'address2': '这是另一个测试用的地址嗯',
}


og = Generator(orangers)
odg = Generator(odrangers)
oag = Generator(oarangers)

orders = []
details = []
addresses = []

for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 100
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))

for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 200
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))

for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 300
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))

for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 400
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))

for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 500
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))


for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 600
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))


for i in range(1, 61):
    while True:
        o = og.generate()
        order_id = svc.generate_order_no(o.created_at, o.user_id)
        if order_id not in order_ids:
            order_ids.add(order_id)
            break
        time.sleep(0.2)
    o.id = order_id
    if o.preprocess_state == 200:
        o.order_state = 610
    s = to_xml(o)

    d = odg.generate()
    d.order_id = order_id

    a = oag.generate()
    a.order_id = order_id

    orders.append(to_xml(o).decode('UTF-8'))
    details.append(to_xml(d).decode('UTF-8'))
    addresses.append(to_xml(a).decode('UTF-8'))


print('<?xml version="1.0" encoding="UTF-8"?>')
print('<dataset>')
print('<table name="order">')
print('<rows>')
print(''.join(orders))
print('</rows>')
print('</table>'
)
print('<table name="order_detail">')
print('<rows>')
print(''.join(details))
print('</rows>')
print('</table>')

print('<table name="order_address">')
print('<rows>')
print(''.join(addresses))
print('</rows>')
print('</table>')

print('</dataset>')
