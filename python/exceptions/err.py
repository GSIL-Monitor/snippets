# -*- coding: utf-8 -*-


def hello():
    err = None
    print('0: {}'.format(locals()))
    try:
        b = 2
        print('1: {}'.format(locals()))
        raise ValueError()
        print('2: {}'.format(locals()))
    except ValueError as err:
        print('3: {}'.format(locals()))
        pass
    print('4: {}'.format(locals()))
    return '', err


hello()
