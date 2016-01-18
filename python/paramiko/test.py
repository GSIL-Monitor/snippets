# -*- coding: utf-8 -*-
import socket
import paramiko

# open socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_CLOEXEC)
sock.connect(('example.com', 22))

# create transport and start client
t = paramiko.transport.Transport(sock)
t.start_client()

# key-based auth
agent = paramiko.agent.Agent()
agent_keys = agent.get_keys()


for key in agent_keys:
    t.auth_publickey(username='foo', key=key)
