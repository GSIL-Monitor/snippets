# -*- coding: utf-8 -*-
import time
import importlib

while True:
    import b
    b.app.do_something()
    time.sleep(1)
    importlib.reload(b)
