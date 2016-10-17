# -*- coding: utf-8 -*-
import argparse
import socket
import sys
import logging
import time


sock = None
mc_host = '127.0.0.1'
mc_port = 11211
st_host = '127.0.0.1'
st_port = 8125


ap = argparse.ArgumentParser()
ap.add_argument('-m', '--memcached', help='memcached server host[:port]', required=True)
ap.add_argument('-n', '--name', help='node name, example: n1368', required=True)
ap.add_argument('-s', '--statsd', help='statsd server host[:port]', required=True)
ap.add_argument('-d', '--dry', help='dry run, show detail, not sending metrics', action='store_true')

options = ap.parse_args()

_ = options.memcached.split(':')

if len(_) == 1:
    mc_host = _[0]
else:
    mc_host, mc_port = _

_ = options.statsd.split(':')

if len(_) == 1:
    st_host = _[0]
else:
    st_host, st_port = _


def send_metric(name, value):
    global st_host, st_port
    _ = name % value
    msg = _.encode('ascii')

    if options.dry:
        print(msg)
    else:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM | socket.SOCK_CLOEXEC)
        sock.sendto(msg, (st_host, st_port))


def conn():
    global sock, mc_host, mc_port
    sock = None
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM | socket.SOCK_CLOEXEC)
    try:
        sock.connect((mc_host, mc_port))
    except Exception as err:
        logging.exception('')
        time.sleep(2)
        conn()


monitor_items = [
    'curr_connections',
    'total_connections',
    'cmd_get',
    'cmd_set',
    'get_cmd',
    'set_cmd',
    'get_hits',
    'get_misses',
    'bytes_read',
    'bytes_written',
    'accepting_conns',
    'curr_items',
    'total_items',
    'evictions',
    'reclaimed'
]



conn()

_ = b'stats\n'
sock.send(_)

a = sock.recv(10240)
lines = a.decode('ascii').split('\r\n')

for line in lines:
    _ = line.split(' ')
    if len(_) != 3:
        continue
    __, k, v = _

    if k in monitor_items:
        name = 'db.memcached.%s.%s' % (options.name, k) + ':%s|g'
        value = v
        send_metric(name, value)
