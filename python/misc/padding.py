# -*- coding: utf-8 -*-

def padding(payload, length, d=None):
    if type(payload) != list:
        raise RuntimeError('cannot padding payload that is not a list')

    if len(payload) >= length:
        return payload

    for i in range(length - len(payload)):
        payload.append(d)

    return payload


print(padding([1, 2, 3], 2))
print(padding([1, 2, 3], 3))
print(padding([1, 2, 3], 4))
print(padding([1, 2, 3], 5))
