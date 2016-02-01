# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import pickle
import struct
import sys


def format(attr):
    attr['message'] = logging.makeLogRecord(attr).getMessage()
    attr['time'] = datetime.fromtimestamp(attr['created'])

    fmt = ('[%(time)s %(levelname)-7s (%(name)s) '
           '<%(process)d> %(filename)s:%(lineno)d] %(message)s')

    return fmt % attr


while True:
    dgram_size = sys.stdin.read(4)
    if len(dgram_size) < 4:
        break
    slen = struct.unpack('>L', dgram_size)[0]
    data = sys.stdin.read(slen)

    while len(data) < slen:
        data = data + sys.stdin.recv(slen - len(data))

    t = pickle.loads(data)
    # print(t)
    print(format(t))
