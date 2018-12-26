# -*- coding: utf-8 -*-
import random

WHITESPACE = [' ', '\n', '\t', '\r']

def chaoslog(msg):
    out = []
    out.append(msg[0])
    for i in range(1, len(msg)):
        if i in WHITESPACE:
            continue
        x = random.randint(0, 3)
        out.append(' ' * x)
        out.append(msg[i])

    line = ''.join(out)
    return line


if __name__ == '__main__':
    msg = '这句话就是毒瘤'
    for i in range(10):
        print(chaoslog(msg))
