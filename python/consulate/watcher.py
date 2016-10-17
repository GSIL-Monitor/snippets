# -*- coding: utf-8 -*-
import json
import logging

import consulate


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(levelname)-05s] %(message)s')

consul = consulate.Consul()

def get_all_services():
     rv = None
     body = consul.catalog.services()
     if body:
          _ = json.loads(body.decode('UTF8'))
          if _:
               rv = []
               for key in _.keys():
                    rv.append(key)
               return rv

def get_available_instances(service_id):
     body = consul.health.service(service_id, passing=True)
     if not body:
          return

     instances = json.loads(body.decode('UTF8'))
     logging.info('%s: %s' % (service, len(instances)))

     if len(instances) < 0:
          return

     rv = {}

     for i in instances:
          _ = i['Service']
          for tag in _['Tags']:
               if tag in rv:
                    rv[tag].append(dict(addr=_['Address'], port=_['Port']))
               else:
                    rv[tag] = [dict(addr=_['Address'], port=_['Port'])]

     return rv

rv_services = {}
services = get_all_services()
for service in services:
     # skip consul
     if 'consul' == service:
          continue

     instances = get_available_instances(service)
     if instances:
          rv_services[service] = instances

logging.info(rv_services)

session = consulate.Session()

def get_all_service_keys():
     prefix = 'services/'

     _ = session.kv.find(prefix, keys=True)
     if _ == []:
          return

     records = json.loads(_.decode('UTF8'))

     logging.info(records)

     return records

records = get_all_service_keys()

logging.info(records)

def clean_outdated_keys(recoard):
     logging.info('start cleaning outdated keys')
     if not records:
          return

     for _ in records:
          service, tag = _.replace('services/', '').split('/', 1)

          if service not in rv_services:
               key = 'services/%s' % service
               logging.info('deleting key: %s' % key)
               session.kv.delete(key, recurse=True)
               continue

          if tag not in rv_services[service]:
               key = 'services/%s/%s' % (service, tag)
               logging.info('deleting key: %s' % key)
               session.kv.delete(key, recurse=True)


clean_outdated_keys(records)

for service in rv_services:

     for tag in rv_services[service]:

          key = 'services/%s/%s' % (service, tag)
          logging.info('writing key: %s' % key)
          session.kv.set_record(key, value=rv_services[service][tag])
