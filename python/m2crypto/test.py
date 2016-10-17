# -*- coding: utf-8 -*-
from M2Crypto import SMIME, Rand
from pysmime.util import BIO_from_buffer

def sign(cert_file, key_file, message, flags):
    """
    Returns a der encoded signed message
    """
    signer = SMIME.SMIME()
    signer.load_key(key_file, cert_file)
    Rand.load_file('randpool.dat', -1)
    p7 = signer.sign(BIO_from_buffer(message), flags=flags)
    Rand.save_file('randpool.dat')
    signed_message = BIO_from_buffer()
    p7.write_der(signed_message)
    return signed_message.read()

print(sign('momoka.net.cert.pem', 'momoka.net.key.pem', 'hello', 0))
