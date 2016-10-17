# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep

from fluent import sender
from fluent import event



# for local fluent
sender.setup('alog')

# for remote fluent
# sender.setup('app', host='127.0.0.1', port=24224)


# send event to fluentd, with 'app.follow' tag
while True:
    event.Event('parsed', {'host': 'api.anjuke.com',
                           'datetime': str(datetime.now())})
