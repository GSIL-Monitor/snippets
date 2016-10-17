 # -*- coding: utf-8 -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import sys
import random
import time

from twisted.internet import interfaces, defer, reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.python.log import startLogging
from zope.interface import implements



article = """
Nevada served in both World Wars: during the last few months of World War I, Nevada was based in Bantry Bay, Ireland, to protect the supply convoys that were sailing to and from Great Britain. In World War II, she was one of the battleships trapped when the Japanese attacked Pearl Harbor. She was the only battleship to get underway during the attack, making the ship "the only bright spot in an otherwise dismal and depressing morning" for the United States.[13] Still, she was hit by one torpedo and at least six bombs while steaming away from Battleship Row, forcing her to be beached. Subsequently salvaged and modernized at Puget Sound Navy Yard, Nevada served as a convoy escort in the Atlantic and as a fire-support ship in four amphibious assaults: the Normandy Landings and the invasions of Southern France, Iwo Jima, and Okinawa."""

_ = filter(lambda x: len(x) > 0, article.split(' '))
words = set()
for __ in _:
    words.add(__)

words = list(words)

def wait(seconds, result=None):
    """Returns a deferred that will be fired later"""
    d = defer.Deferred()
    reactor.callLater(seconds, d.callback, result)
    return d

class RandomWords(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def connectionMade(self):
        print('connection made')


    def dataReceived(self, data):
        idx = int(random.random() * len(words))
        rv = words[idx]
        self.transport.write(rv + '\n')


    def connectionLost(self, reason):
        print('connecton lost: %s' % reason)


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = RandomWords
    reactor.listenTCP(9000, factory)
    print('server started at tcp://*:9000')
    startLogging(sys.stdout)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
