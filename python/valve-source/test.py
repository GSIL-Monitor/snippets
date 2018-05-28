# -*- coding: utf-8 -*-
import pprint

from valve.source.a2s import ServerQuerier


server = ServerQuerier(('dyn.momoka.net', 27016))
_ = server.ping()
print(_)

_ = server.info()
pprint.pprint(_.values)

_ = server.players()
for player in _['players']:
    pprint.pprint(player.values)
