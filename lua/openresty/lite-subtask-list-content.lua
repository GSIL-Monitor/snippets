--
-- 2018-06-19
-- 钱咖 iOS dashboard 页面(API)级缓存
-- !! 本文件前部定义变量与函数，最下部才是请求的处理逻辑 !!
--
local json = require('cjson')
local redis = require('resty.redis')
local strlen = string.len

-- == 函数定义 ==
-- 返回以下格式的 table
-- {
--   status: int,    // HTTP状态
--   headers: table, // 响应头
--   body: str,      // 响应内容
-- }

local function makeAlive(client)
  -- 将 redis 连接设置为保持连接，并放进连接池
  -- https://github.com/openresty/lua-resty-redis#set_keepalive
  -- FIXME: 空闲时间与连接池大小走配置
  client:set_keepalive(10000, 1000)
end


local function rawBackend()
  -- dashboard 原始后端的响应内容

  -- TODO: proxy_set_header
  -- Host
  -- X-Real-Ip
  -- X-Forwarded-For
  -- X-Forwarded-Host

  local res = ngx.location.capture('/_raw_lite_subtask_list')
  local rv = {}
  rv['body'] = res.body
  rv['status'] = res.status
  rv['headers'] = res.header
  return rv
end

-- 返回以下格式的 table
-- {
--   status: int,    // HTTP状态
--   headers: table, // 响应头
--   body: str,      // 响应内容
-- }
local function cacheBackend(cookie)
  local client = redis:new()
  -- FIXME: 这里连接地址先写死本机，后面考虑走配置？
  local ok, err = client:connect('127.0.0.1', 6379)
  if not ok then
    error('failed to connect: ' .. (err or 'unknown'))
    return
  end

  local cacheKey = "resty:" .. cookie
  -- FIXME: 缓存时间走配置
  local expire = 5

  local blob, err = client:get(cacheKey)
  if not blob then
    -- 这里指连接异常
    -- TODO: 连接异常的时候直接走原始后端？
    error('failed to connect: ' .. (err or 'unknown'))
    return
  end

  local body, status, headers, data

  if blob == ngx.null then
    -- 没有命中缓存，从后端获取
    local resp = rawBackend()
    body = resp.body
    status = resp.status
    headers = resp.headers
    if status == ngx.HTTP_OK then
      -- 只有后端返回 200 状态时，才能写入缓存
      local payload = json.decode(body)
        -- 后端返回的 err_code 为 0 的时候才能写入缓存
        if payload['err_code'] == 0 then
        -- NOTE: 缓存内容里不能包含 messages
        -- 否则用户会看到多次一样的消息
        -- NOTE: lua 默认 JSON 编码不支持空数组
        -- json.empty_array 写法只在 resty-cjson 中有效
        -- 原始的 lua-cjson 并不支持
        -- 参考：
        -- https://github.com/mpx/lua-cjson/issues/11#issuecomment-296559240
        payload['messages'] = json.empty_array
        newBody = json.encode(payload)
        newHeaders = {}
        for k, v in pairs(headers) do
          newHeaders[k] = headers[k]
        end
        -- Content-Length 头需要重新计算
        newHeaders['Content-Length'] = strlen(newBody)
        data = {}
        data['status'] = status
        data['headers'] = newHeaders
        data['body'] = newBody
        local blob = json.encode(data)

        -- FIXME: 检查设置结果？
        client:set(cacheKey, blob)
        -- redis 不支持设置缓存同时设置超时
        -- 需要单独设置
        client:expire(cacheKey, expire)
      end
    end
    headers['X-Qianka-Resty'] = 0
  else
    -- 命中缓存，解码使用
    data = json.decode(blob)
    body = data['body']
    status = data['status']
    headers = data['headers']
    headers['X-Qianka-Resty'] = 1
  end

  local rv = {}
  rv['body'] = body
  rv['status'] = status
  rv['headers'] = headers

  -- NOTE: redis 连接池只能在最后设置
  -- 否则调用后会报连接已关闭
  makeAlive(client)

  return rv
end

-- !!=== 请求处理逻辑从这里开始 ===!!

-- 先获取 cookie 内容
local cookie = ngx.var.cookie_DIS4

if not cookie then
  -- 没有 cookie 的时候直接返回后端内容？
  -- TODO: 没有 cookie 的时候也设置一下缓存？
  -- NOTE: 如果这里只处理 dashboard ，没有 cookie 的时候只会返回 401 状态
  resp = rawBackend()
else
  resp = cacheBackend(cookie)
end

-- 输出响应内容
ngx.status = resp.status
for k, v in pairs(resp.headers) do
  ngx.header[k] = v
end
ngx.say(resp.body)
