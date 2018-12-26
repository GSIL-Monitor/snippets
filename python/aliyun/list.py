# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import pprint

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import simplejson as json

import colors


API_KEY = '9L9ncr4PXC1x7num'
API_SECRET = 'e4tnvD2O3dKNWWMtZKMsNQcc3WmVPr'

regions = [
    'cn-hangzhou',
    'cn-shanghai',
    'cn-hongkong',
    'cn-qingdao',
    'us-west-1',
]

# 中国标准时区 +8
CST = timezone(timedelta(hours=8))


def utc2cst(dt):
    dt = dt.replace(tzinfo=timezone.utc)
    rv = dt.astimezone(CST)
    return rv


def query_hosts():
    rv = []
    acs = client.AcsClient(API_KEY, API_SECRET, 'cn-hangzhou')
    kls = DescribeInstancesRequest.DescribeInstancesRequest
    page = 1
    while True:
        request = kls()
        request.set_accept_format('json')
        request.set_PageSize(100)
        request.set_PageNumber(page)

        result = acs.do_action_with_exception(request)
        body = json.loads(result.decode('utf-8'))

        instances = body['Instances']['Instance']
        if len(instances) <= 0:
            break

        for instance in instances:
            rv.append(instance)

        page += 1

    return rv


def parse(host):
    dt = datetime.strptime(host['ExpiredTime'], '%Y-%m-%dT%H:%MZ')
    dt = utc2cst(dt)
    _ = {
        'InstanceName': host['InstanceName'],
        'ExpiredTime': dt.strftime('%Y-%m-%d %H:%M:%S'),
        'ZoneId': host['ZoneId'],
        'NetworkType': host['InstanceNetworkType'],
    }
    return _


hosts = query_hosts()
hosts = [y for y in filter(
    lambda x: x['NetworkType'] == 'classic', [parse(x) for x in hosts])]
def mySort(host):
    return host['ExpiredTime'], host['InstanceName']

hosts = sorted(hosts, key=mySort)

o = defaultdict(list)
for host in hosts:
    dt = host['ExpiredTime']
    hostname = host['InstanceName']
    if host['ZoneId'] == 'cn-hangzhou-c':
        hostname += colors.red('[C]')
    o[dt].append(hostname)



for d in sorted(o.keys()):
    print('{}:\t{}'.format(d, ', '.join(sorted(o[d]))))
