# -*- coding: utf-8 -*-
import lzma

from flask import Flask, request

b = b''
with open('data.txt', 'rb') as f:
    b = f.read()

app = Flask(__name__)

@app.route('/')
def index():
    z = int(request.args.get('zlevel', '6'))
    _ = lzma.compress(b, preset=z)
    print("%d : %d", len(b), len(_))
    return ''
