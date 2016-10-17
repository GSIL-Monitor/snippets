# -*- coding: utf-8 -*-
import dns.resolver
import argparse

ap = argparse.ArgumentParser()

ap.add_argument('-n', '--nameserver', default='114.114.114.114')

options = ap.parse_args()

r = dns.resolver.Resolver()

r.nameservers = [options.nameserver]
r.port = 53

with open('hosts.txt') as f:
    for line in f:
        hostname = line.strip()

        if not hostname.endswith('ops.gaoshou.me'):
            hostname += '.ops.gaoshou.me'


        try:
            ans = r.query('h' + hostname)
            internal_ip = ans.response.answer[0].to_text().split(' ')[-1]
        except dns.resolver.NXDOMAIN:
            internal_ip = null

        try:
            ans = r.query('n' + hostname)
            external_ip = ans.response.answer[0].to_text().split(' ')[-1]
        except dns.resolver.NXDOMAIN:
            external_ip = null

        print('%s\t%s\t%s' % (hostname.replace('.ops.gaoshou.me', ''), internal_ip, external_ip))
