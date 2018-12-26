# -*- coding: utf-8 -*-
import contextlib


# class MyCtx(contextlib.ContextManager):
class MyCtx(object):

    def __enter__(self):
        print('MyCtx __enter__')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('MyCtx __exit__')
        return


with MyCtx() as f:
    print(f)
