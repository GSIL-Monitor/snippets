# -*- coding: utf-8 -*-
import pickle
import socketserver
import time


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        print('got new request length: %s' % len(data))
        # print('got new request: %s' % data)
        try:
            time.sleep(1)
        except pickle.UnpicklingError:
            pass


s = socketserver.UDPServer(('127.0.0.1', 8129), MyUDPHandler)
s.serve_forever()
