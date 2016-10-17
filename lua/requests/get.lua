-- package.cpath = package.cpath .. ';/tmp/lua/lib/lua/5.2/?.so'
-- package.path = package.path .. ';/tmp/lua/share/lua/5.2/?.lua'
print(package.path)
print(package.cpath)

local requests = require('requests')

local res = requests.get('http://localhost/proxy.pac')
print(res.status_code)
print(res.text)
