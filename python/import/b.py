# -*- coding: utf-8 -*
import c

class App(object):
    # hello = None

    def do_something(self):
        service = c.Service()
        print(hasattr(service, 'func'))


app = App()
