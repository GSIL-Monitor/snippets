#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib
import json
import logging
import pprint
import re
import time

import pika
import pylibmc


EXPIRE = 10


COUNT = 0
mc = pylibmc.Client(['127.0.0.1'], binary=True, behaviors={
    'tcp_nodelay': True,
    'ketama': True,
})

# This is the function that basic_consume will send messages to
def process_message(ch, method, header, body):


    payload = json.loads(body.decode('utf-8'))
    dieid = payload['dieid']

    key = 'dieid:%s' % dieid
    _ = mc.get(key)
    if _ is None:
        mc.set(key, 1, EXPIRE)

    return

    # pprint.pprint(payload['installed_apps'])

    if type(payload['installed_apps']) is str:
        return

    bundle_ids = sorted(map(lambda x: x['bundle_id'],
                            payload['installed_apps']))
    _ = ''.join(bundle_ids).encode('utf-8')
    m = hashlib.md5()
    m.update(_)
    h = m.hexdigest()
    key = 'dieid:%s:%s' % (dieid, h)
    _ = mc.get(key)
    if _ is None:
        mc.set(key, 1, EXPIRE)


def main():
    # Rabbit Server to connect to
    host = 'n1416.ops.gaoshou.me'
    port = 5672

    # # Exchange and queue information
    exchange_name = 'hera.topic'
    routing_key = 'keys.state'
    exchange_type = 'topic'
    queue_name = 'lppa.test'

    # Let's set this up by default, we'll use it later
    process_messages = True

    # Connect to Rabbit
    connection= pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, virtual_host='/'))

    # Create a channel to talk to Rabbit on
    channel = connection.channel()

    # # Create our exchange
    # channel.exchange_declare( exchange = exchange_name,
    #         type = exchange_type,
    #         durable = False,
    #         auto_delete = True)

    # Create our Queue
    rv = channel.queue_declare(
            queue = queue_name ,
            durable = False,
            exclusive = False,
            auto_delete = True )

    # queue_name = rv.method.queue

    # Bind to the Queue / Exchange
    channel.queue_bind(
        queue = queue_name,
        exchange = exchange_name,
        routing_key = routing_key )

    # Let AMQP know to send us messages
    channel.basic_consume(consumer_callback=process_message,
                          queue=queue_name,
                          no_ack=True)

    # Wait for a message
    channel.start_consuming()

    # Close the channel
    channel.close()

    # Close our connection
    connection.close()

# This might go somewhere like a signal handler
def cancel_processing():
    """ Stop consuming messages from RabbitMQ """
    global channel, consumer_tag, process_messages

    # Do this so we exit our main loop
    process_message = False

    # Tell the channel you dont want to consume anymore
    channel.basic_cancel( consumer_tag )


if __name__ == '__main__':
    main()
