# -*- coding: utf-8 -*-
from test import app

app.config['DEBUG'] = True
app.prepare()
app.run('0.0.0.0', port=3000, threaded=True)
