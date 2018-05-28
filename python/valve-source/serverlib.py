# -*- coding: utf-8 -*-
import pprint

from valve.source.a2s import ServerQuerier


class ServerLib(object):

    def __init__(self, address):
        self.address = address
        self.server = ServerQuerier(address)
        self.server.ping()

    def getInfo(self):
        _ = self.server.info()
        return _.values

    def getPlayers(self):
        rv = []
        _ = self.server.players()
        for player in _['players']:
            rv.append(player.values)
        return rv
