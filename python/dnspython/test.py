# -*- coding: utf-8 -*-

from dns import rdataclass, rdatatype, resolver, rrset

r = resolver.Resolver()

r.nameservers = ['127.0.0.1']
r.port = 53

answer = resolver.query('www.google.com')

print(answer.response.answer[0].to_rdataset())
