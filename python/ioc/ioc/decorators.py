# -*- coding: utf-8 -*-
from ioc import BeanObject

def Bean(*args, **kwargs):
    invoked = bool(not args or kwargs)

    # print("===> Bean")
    # print(args)
    # print(kwargs)

    if not invoked:
        func, args = args[0], ()

    def wrapper(func):

        def new_func(*_args, **_kwargs):

            # print("===> new_func")
            # print(_args)
            # print(_kwargs)

            rv = func(*_args, **_kwargs)
            return rv

        name = func.__name__
        if 'name' in kwargs:
            name = kwargs.pop('name')

        # new_func.__name__ = name
        # new_func.__module__ = func.__module__

        return BeanObject(name, new_func, *args, **kwargs)

    return wrapper if invoked else wrapper(func)
