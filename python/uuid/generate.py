# -*- coding: utf-8 -*-
import uuid

cnt = 0

with open('tokens.txt', 'w') as f:
    for i in range(700000):
        token = str(uuid.uuid4()).replace('-', '') * 2
        f.write(token + '\n')
        cnt += 1
        if cnt % 10000 == 0:
            print(cnt)

print('done')
