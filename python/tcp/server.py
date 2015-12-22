# -*- coding: utf-8 -*-
import random
import socket
import time
import sys


article = """
Nevada served in both World Wars: during the last few months of World War I, Nevada was based in Bantry Bay, Ireland, to protect the supply convoys that were sailing to and from Great Britain. In World War II, she was one of the battleships trapped when the Japanese attacked Pearl Harbor. She was the only battleship to get underway during the attack, making the ship "the only bright spot in an otherwise dismal and depressing morning" for the United States.[13] Still, she was hit by one torpedo and at least six bombs while steaming away from Battleship Row, forcing her to be beached. Subsequently salvaged and modernized at Puget Sound Navy Yard, Nevada served as a convoy escort in the Atlantic and as a fire-support ship in four amphibious assaults: the Normandy Landings and the invasions of Southern France, Iwo Jima, and Okinawa."""

port = 9000
if len(sys.argv) > 1:
    port = int(sys.argv[1])

_ = filter(lambda x: len(x) > 0, article.split(' '))
words = set()
for __ in _:
    words.add(__)

words = list(words)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_CLOEXEC)
sock.bind(('localhost', port))

sock.listen(5)

while True:
    conn, addr = sock.accept()
    while True:
        idx = int(random.random() * len(words))
        rv = words[idx]
        try:
            conn.send((rv + '\n').encode('ascii'))
        except BrokenPipeError:
            break
        time.sleep(0.001)
