# -*- coding: utf-8 -*-
from confluent_kafka import Consumer, KafkaError


c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'default.topic.config': {
        'auto.offset.reset': 'earliest'
        # 'auto.offset.reset': 'smallest'
    }
})

c.subscribe(['test'])

while True:
    msg = c.poll(1.0)

    print(msg)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
