# -*- coding: utf-8 -*-
import hashlib
import pprint
import requests
import time

SHARED_KEY = '5486e15ec3a442fd8c684d51c18970ba'

def sign_payload(method, payload):
    parameters = []
    for k in sorted(payload.keys()):
        v = payload.get(k)
        parameters.append('%s=%s' % (k, v))

    _ = '%s%s%s' % (method, '+'.join(parameters), SHARED_KEY)
    print(_)
    m = hashlib.md5()
    m.update(_.encode('utf-8'))
    return m.hexdigest().upper()

payload = dict(
    timestamp=int(time.time()),
    qk_id=34343008,
    order_sn='test_order_sn_1',
    pay_price=12.34,
    status=0,
    commission=234.56,
    create_time='2016-02-16 15:09:02',
    item_num=10,
    item_title='测试商品名称001',
    num_iid='测试淘宝商品id001',
    seller_shop_title='测试店铺名称001',
)


method = '/fanli/order.push'

sign = sign_payload(method, payload)

payload['sign'] = sign

pprint.pprint(payload)

res = requests.post('http://n1409.ops.gaoshou.me/fanli/order.push',
                    data=payload)

pprint.pprint(res.status_code)
pprint.pprint(res.json())
