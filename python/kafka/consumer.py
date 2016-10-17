# -*- coding: utf-8 -*-
from kafka import KafkaClient, SimpleConsumer

client = KafkaClient('127.0.0.1:9092')

consumer = SimpleConsumer(client, 'test-group', 'test')

cnt = 0

while True:
    try:
        for message in consumer:
            cnt += 1
            print(message.message.value)
    except:
        import time
        import warnings
        warnings.warn('error')
        time.sleep(1)
