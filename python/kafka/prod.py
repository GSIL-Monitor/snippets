# -*- coding: utf-8 -*-
from kafka import KafkaClient, SimpleProducer
from kafka import KeyedProducer

client = KafkaClient('127.0.0.1:9092')

prod = SimpleProducer(client)

from datetime import datetime

for i in range(10):
    prod.send_messages('test', str(datetime.now()).encode('ascii'))
