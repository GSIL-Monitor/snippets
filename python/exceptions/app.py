# -*- coding: utf-8 -*-


class CustomError(Exception):
    pass

class AnotherError(CustomError):
    pass



def hello():
    raise AnotherError()


try:
    hello()
except CustomError:
    pass
