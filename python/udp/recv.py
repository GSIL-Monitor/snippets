# -*- coding: utf-8 -*-
import socketserver
import time

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        print('got new request: %s' % data)
        try:
            time.sleep(10)
        except pickle.UnpicklingError:
            pass

s = socketserver.UDPServer(('127.0.0.1', 4000), MyUDPHandler)
s.serve_forever()
