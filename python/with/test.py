# -*- coding: utf-8 -*-

class A(object):

    def __enter__(self, *args):
        print('enter: %s' % str(args))
        pass

    def __exit__(self, *args):
        print('exit: %s' % str(args))
        pass


with A() as a:
    print(a)
