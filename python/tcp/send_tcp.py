# -*- coding: utf-8 -*-
import socket
import sys
import logging
import time
import uuid

sock = None

def conn():
    global sock
    sock = None
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM | socket.SOCK_CLOEXEC)


    try:
        sock.connect(('127.0.0.1', 9999,))
    except Exception as err:
        logging.exception('')
        time.sleep(2)
        conn()

conn()

idfa = str(uuid.uuid4()).upper()
apple_id = 123
status = 0

req = 'set_idfa:%s,%d,%d\n' % (idfa, apple_id, status)
_ = req.encode('UTF-8')
logging.warning(_)

sock.send(_)
sock.send(_)
res = b''
while True:
    _ = sock.recv(1)
    res += _
    if _ == b'\n':
        _ = res.strip().decode('UTF-8')
        logging.warning(_)
        res = b''
