# -*- coding: utf-8 -*-
import json
import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for line in sys.stdin:
    a = line.strip()
    record = {'task_id': 'example1', 'msg': a, 'time': str(int(time.time()))}
    payload = json.dumps(record)
    sock.sendto(payload.encode('UTF-8'), ('127.0.0.1', 5006))
