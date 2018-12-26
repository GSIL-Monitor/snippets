local io = require 'io'; local handle = io.popen('ls'); local result = handle:read() ;print(result); handle:close()
