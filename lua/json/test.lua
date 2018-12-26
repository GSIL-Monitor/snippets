package.path = package.path ..
  ";/home/momoka/src/lua/lua-resty-libcjson/lib/resty/?.lua"

local json = require 'libcjson'

local blob = '{"a": [], "b": [1, 2, 3], "c": {"k1": 1}, "d": {}}'
local s = json.encode(json.decode(blob), false)
print(s)
