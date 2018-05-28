# -*- coding: utf-8 -*-
# import pprint
from collections import OrderedDict

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import config
from serverlib import ServerLib


webapp = Flask(__name__)

webapp.config.from_object(config)
Bootstrap(webapp)


@webapp.route('/')
def index():

    server = ServerLib(webapp.config['SERVER'])
    info = server.getInfo()

    # pprint.pprint(info)

    serverInfo = OrderedDict()
    for key in sorted(info.keys()):
        serverInfo[key] = info[key]

    players = server.getPlayers()

    return render_template('index.html', info=serverInfo, players=players)
