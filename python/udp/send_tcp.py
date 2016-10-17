# -*- coding: utf-8 -*-

import socket
import sys
import logging
import time


sock = None

def conn():
    global sock
    sock = None
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM | socket.SOCK_CLOEXEC)
    try:
        sock.connect(('10.169.9.138', 5006))
    except Exception as err:
        logging.exception('')
        time.sleep(2)
        conn()



conn()
for line in sys.stdin:
    _ = line.encode('utf8')
    try:
        sock.send(_)
    except Exception as err:
        logging.exception('')
        time.sleep(2)
        conn()
