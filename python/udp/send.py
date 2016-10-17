# -*- coding: utf-8 -*-

import socket
import sys

sock = None


def conn():
    global sock
    sock = None
    sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

conn()

for line in sys.stdin:
    _ = line.encode('utf8')
    # sock.sendto(_, ('121.41.123.27', 5005)) # h1397
    sock.sendto(_, ('127.0.0.1', 4000)) # h1397
