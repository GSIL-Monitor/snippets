# -*- coding: utf-8 -*-

import subprocess
from subprocess import PIPE


OPENSSL_BINARY = '/usr/bin/openssl'


def run_command(command, stdin=None):

    if stdin and type(stdin) != bytes:
        raise RuntimeError('please encode stdin first')

    _ = command.split()
    p = subprocess.Popen(_, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    if stdin:
        stdout, stderr = p.communicate(input=stdin)
    else:
        stdout, stderr = p.communicate()
    return stdout


def smime_sign(cert, key, message):
    command = '%s smime -sign -signer %s -inkey %s -outform der -nodetach' %\
      (OPENSSL_BINARY, cert, key)

    return run_command(command, stdin=message)


def smime_verify(signed, cafile):

    command = '%s smime -verify -CAfile %s -inform dec -noverify -binary' %\
      (OPENSSL_BINARY, cafile)

    return run_command(command, stdin=signed)

_ = smime_sign('momoka.net.cert.pem', 'momoka.net.key.pem', b'hello world')
print(type(_))
print(_)

# smime_verify('momoka.net.cert.pem', )
