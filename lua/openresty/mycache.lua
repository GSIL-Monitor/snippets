local _M = {}
local lrucache = require "resty.lrucache"
local c, err = lrucache.new(200)
if not c then
  return error("failed to create the cache: " .. (err or "unknown"))
end

function _M.set(key, value, timeout)
  c:set(key, value, timeout)
end

function _M.get(key)
  return c:get(key)
end

return _M
