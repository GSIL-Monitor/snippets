# -*- coding: utf-8 -*-
import json
import random
import socket
import sys
import time



payload = {
    'flag': 'middleware',
    'date': '2015-12-24 00:00:00',
    'data': {
        'user_id': 1234567890
    }
}

port = 9000
if len(sys.argv) > 1:
    port = int(sys.argv[1])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_CLOEXEC)
sock.bind(('localhost', port))

sock.listen(5)

while True:
    conn, addr = sock.accept()
    while True:

        rv = json.dumps(payload)

        try:
            conn.send((rv + '\n').encode('ascii'))
        except BrokenPipeError:
            break
        time.sleep(0.1)
