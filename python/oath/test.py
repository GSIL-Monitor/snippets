# -*- coding: utf-8 -*-
import oath

secret = 'MMYGIOJWMQ4WCNLE'
ga = oath.google_authenticator.from_b32key(secret)
token = ga.generate()
print(token)
