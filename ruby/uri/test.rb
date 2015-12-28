# coding: utf-8
require 'addressable/uri'
require 'unirest'


Unirest.clear_default_headers()


u = Addressable::URI.new
u.host = 'n1391.ops.gaoshou.me:8000'
u.path = 'render'
u.query_values = {
  :format => 'json',
  :from => '-1min',
  :util => 'now',
  :target => 'collectd.h1386.memory.memory-{used,free}'
}
u.scheme = 'http'

p u

p u.to_s

url = u.to_s
res = Unirest.get(url)

p res
p res.code
p res.raw_body
