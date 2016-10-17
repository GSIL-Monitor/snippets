#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 - AleiPhoenix <aleiphoenix@gmail.com>

import pika
import json
import re
import datetime

# This is the function that basic_consume will send messages to
def process_message( message ):
    """ Callback function used by channel.basic_consume """
    print(message.body)


def main():
    # Rabbit Server to connect to
    host = '192.168.1.56'
    port = 5676

    # # Exchange and queue information
    exchange_name = 'nydus.58.service.internal.community '
    routing_key = '#'
    exchange_type = 'topic'
    queue_name = "chenlei"

    # Let's set this up by default, we'll use it later
    process_messages = True

    # Connect to Rabbit
    connection= amqp.Connection( host ='%s:%s' % ( host, port ),
            # userid = 'guest',
            # password = 'guest',
            ssl = False,
            virtual_host = '/' )

    # Create a channel to talk to Rabbit on
    channel = connection.channel()

    # # Create our exchange
    # channel.exchange_declare( exchange = exchange_name,
    #         type = exchange_type,
    #         durable = False,
    #         auto_delete = True)

    # Create our Queue
    channel.queue_declare( queue = queue_name ,
            durable = False,
            exclusive = False,
            auto_delete = True )

    # Bind to the Queue / Exchange
    channel.queue_bind( queue = queue_name,
            exchange = exchange_name,
            routing_key = routing_key )

    # Let AMQP know to send us messages
    consumer_tag = channel.basic_consume( queue = queue_name,
            no_ack = True,
            callback = process_message )

    # Loop while process_messages is True
    while process_messages:

        # Wait for a message
        channel.wait()

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
