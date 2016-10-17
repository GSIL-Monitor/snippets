# -*- coding: utf-8 -*-
from time import sleep, time

TABLE = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 1),
    (5, 2),
    (6, 3),
    (7, 1),
    (8, 2),
    (9, 3),
    (10, 1),
    (11, 2),
    (12, 3),
    (13, 1),
    (14, 2),
    (15, 3),
]



last_id = 0
limit = 2

start = time()

def get_last_id():
    return TABLE[-1][0]

def get_next(last_id, limit):
    return TABLE[last_id:last_id+limit]

def filtered(last_id, limit):
    _ = TABLE[last_id:-1]
    rv = []
    for i in _:
        if i[1] == 3:
            rv.append(i)

    return rv

while True:

    # _ = get_next(last_id, limit)
    _ = filtered(last_id, limit)

    print(_)
    sleep(0.3)

    if _ == []:
        if get_last_id() - last_id > limit:
            last_id += limit
        else:
            last_id = get_last_id()

    for i in _:
        print(i)
        if i[1] == 3:
            print('got 3')
        last_id = i[0]

    if last_id == 15:
        # 最大
        break

end = time()

print('time usage: %s' % (end - start))
