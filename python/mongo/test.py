# -*- coding: utf-8 -*-
import pymongo

mongo = pymongo.MongoClient('n1385.ops.gaoshou.me')

db = mongo['zeus']

for doc in db.crontabs.find({}):
    if doc['crontabs']:
        crontabs = doc['crontabs']
        for row in crontabs:
            cron = row['raw_crontab']
            if 'qk-jobs' in cron:
                print('{}\t{}'.format(doc['hostname'], cron))


# for doc in db.instances.find({}):
#     name = doc['name']
#     print('{}\t{}'.format(doc['hostname'], name))
