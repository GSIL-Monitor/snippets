#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import pprint
import re

import pika



# This is the function that basic_consume will send messages to
def process_message(ch, method, header, body):
    pprint.pprint(ch)
    pprint.pprint(method)
    pprint.pprint(header)
    pprint.pprint(body)


def main():
    # Rabbit Server to connect to
    host = '127.0.0.1'
    port = 5672

    # # Exchange and queue information
    # exchange_name = 'nydus.58.service.internal.community'
    exchange_name = 'amq.topic'
    routing_key = '#'
    exchange_type = 'topic'
    queue_name = 'test'

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
            exclusive = True,
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
