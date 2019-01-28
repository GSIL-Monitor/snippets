# -*- coding: utf-8 -*-
import random
import time

import tqdm

offset = 0
total = 1024 * 1024
with tqdm.tqdm(
        total=total, unit='bit', unit_scale=True, unit_divisor=1024) as bar:
    while offset < total:
        this = random.randint(1, 10000)
        this = min(this, total - offset)
        offset += this
        bar.update(this)
        time.sleep(0.01)
