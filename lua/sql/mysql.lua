-- {{{ add cpath
package.cpath = package.cpath .. ';/tmp/lua/lib/lua/5.2/?.so'
-- }}}

local driver = require 'luasql.mysql'
local env = driver.mysql()

local conn = assert( env:connect('mysql', 'root', '', '127.0.0.1', 3306) )
local cursor, errorString = conn:execute([[SELECT user, host FROM user]])
local rowcount = cursor:numrows()

if rowcount > 0 then
  row = cursor:fetch({}, "a")
  while row do
    print(string.format("user: %s, host: %s", row.user, row.host))
    row = cursor:fetch({}, "a")
  end
end
