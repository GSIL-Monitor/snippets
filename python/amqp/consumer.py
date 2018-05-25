# -*- coding: utf-8 -*-
import argparse
import logging
import sys
import time

from qianka.common.job.rabbitmq import QkRabbitMqConsumer


logger = logging.getLogger(__name__)


class MyConsumer(QkRabbitMqConsumer):

    def __init__(self):
        self.exchange = None
        self.rouing_key = None
        self.sleep = 0
        super().__init__()

    def configure(self, **options):
        if 'exchange' in options:
            self.exchange = options.pop('exchange')
        if 'routing_key' in options:
            self.routing_key = options.pop('routing_key')
        if 'sleep' in options:
            self.sleep = options.pop('sleep')
        super().configure(**options)

    def setup_topology(self):
        self.channel.queue_declare(
            self.queue, auto_delete=True, durable=False)
        self.channel.queue_bind(
            self.queue, self.exchange, routing_key=self.routing_key)

    def handle_message(self, frame, prop, m):
        logger.warn(frame)
        logger.warn(prop)
        logger.warn(m)
        time.sleep(self.sleep)


def main():

    logging.basicConfig(level=logging.INFO)

    ap = argparse.ArgumentParser()
    ap.add_argument('--exchange', required=True)
    ap.add_argument('--routing-key', required=True)
    ap.add_argument('--host', required=True)
    ap.add_argument('--port', type=int, default=5672)
    ap.add_argument('--queue', required=True)
    ap.add_argument('--sleep', default=0, type=float)

    options = ap.parse_args()

    j = MyConsumer()
    j.configure(
        host=options.host,
        port=options.port,
        queue=options.queue,
        exchange=options.exchange,
        routing_key=options.routing_key,
    )
    j.main()


if __name__ == '__main__':
    sys.exit(main())
