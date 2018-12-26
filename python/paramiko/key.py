# -*- coding: utf-8 -*-
from os.path import expanduser

import paramiko

# kf = '/home/momoka/.ssh/qianka/gsbot'
kf = '/home/momoka/.ssh/id_rsa'

# paramiko.RSAKey.from_private_key_file(kf, 'Qianka')
paramiko.RSAKey.from_private_key_file(kf, 'Qianka')

agent = paramiko.Agent()
_ = agent.get_keys()
print(_)

config = paramiko.SSHConfig()

with open(expanduser('~/.ssh/config')) as f:
    config.parse(f)

hostConfig = config.lookup('n1386.ops.gaoshou.me')
print(hostConfig)
