# -*- coding: utf-8 -*-
from redis import StrictRedis

client = StrictRedis.from_url('redis://')
client.decr('1', 1)
