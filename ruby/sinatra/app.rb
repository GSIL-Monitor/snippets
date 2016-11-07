require 'digest'
require 'json'

require 'sinatra'
require 'xz'



IDFA_VERIFY_CONFIG = {
  1 => {
    :ad_id => 1,
    :app_id => 0,
    :is_enabled => true,
    :template_code => '',
    :req_http_method => 'GET',
    :req_idfa_lowercase => true,
    :req_idfa_nohyphen => true,
    :req_idfa_lowercase => true,
    :res_idfa_nohyphen => true,
    :shared_key => 'c2ad26c6-9d4e-4958-94ca-d8c566ab165a'
  },
  2 => {
    :ad_id => 2,
    :app_id => 0,
    :is_enabled => true,
    :template_code => 'jd',
  },
  3 => {
    :ad_id => 3,
    :app_id => 0,
    :is_enabled => true,
    :template_code => 'baidu_ime',
  },
  4 => {
    :ad_id => 4,
    :app_id => 0,
    :is_enabled => true,
    :template_code => 'qijia',
  },
  5 => {
    :ad_id => 5,
    :app_id => 0,
    :is_enabled => true,
    :template_code => 'zhangyue',
  },
}

CLICK_NOTIFY_CONFIG = {
  1 => {
    :is_enabled => true,
    :template_code => '',
    :req_http_method => 'POST',
    :shared_key => 'c2ad26c6-9d4e-4958-94ca-d8c566ab165a'
  },
  2 => {
    :is_enabled => true,
    :template_code => 'base',
    :req_http_method => 'POST',
    :shared_key => 'c2ad26c6-9d4e-4958-94ca-d8c566ab165a'
  },
  3 => {
    :is_enabled => false,
    :template_code => 'base',
    :req_http_method => 'GET',
    :shared_key => 'c2ad26c6-9d4e-4958-94ca-d8c566ab165a'
  },
}


SHARED_KEY = 'c2ad26c6-9d4e-4958-94ca-d8c566ab165a'
cnt = 0

get '/' do
  cnt += 1

  p cnt

  params[:msg]

end

post '/' do
  p params

  request.body.rewind
  p request.body.read

  ''
end

post '/post' do
  p params

  request.body.rewind
  p request.body.read

  params.to_s
end

post '/post-binary' do
  p params
  b = params['body']
  begin
    _ = XZ.decompress(b)
    p _
    p JSON.parse _
  rescue
    p 'xz decompress error!'
  end
  p Digest::MD5.hexdigest b
  params.to_s
end

post '/post_error' do
  403
end

post '/ucweb' do
  JSON.dump({:status => 200, :msg => ''})
end

post '/ucweb_error' do
  JSON.dump({:status => 400, :msg => 'test ucweb error'})
end


post '/test' do
  p headers
  'hello'
end

get '/sleep' do
  sleep 1
  'sleep'
end

put '/put' do
  params.to_s
end

def idfa_verify
  p params.to_s

  if params.include? 'timestamp' then
    m = Digest::MD5.new
    m << params[:appid].to_s
    m << params[:idfa]
    m << params[:timestamp]
    m << SHARED_KEY
    p "#{params[:sign]} <= x => #{m.hexdigest()}"
    if params[:sign] != m.hexdigest() then
      status 400
      {error: true, error_msg: 'sign error'}.to_json
    end
  end

  rv = {}

  params[:idfa].split(',').each do |e|
    rv[e] = 0
  end

  p rv

  rv.to_json
end

post '/idfa-verify' do
  idfa_verify
end
get '/idfa-verify' do
  idfa_verify
end

post '/idfa-qijia' do
  request.body.rewind
  body JSON.parse request.body.read
  p body
  rv = {}
  if body.include? 'idfa' then
    body['idfa'].split(',').each do |e|
      rv[e] = 0
    end
  end

  p rv.to_json

  rv.to_json
end

post '/post-json' do
  request.body.rewind
  body = JSON.parse request.body.read
  p body

  ''
end

post '/post-body' do
  request.body.rewind
  body = request.body.read
  p body

  "i've read your body"
end

put '/ops_api/hosts/:host_id' do
  p params
  request.body.rewind
  body = JSON.parse request.body.read
  p body

  ''
end


get '/ops_api/idfa/verify' do
  p params

  if params[:ad_id].nil? then
    return 404, JSON.dump({:status => 'error', :err_msg => 'params error'})
  end

  ad_id = params[:ad_id].to_i
  if !(IDFA_VERIFY_CONFIG.keys.include? ad_id) then
    return 404, JSON.dump(
             {:status => 'error', :err_msg => 'cannot find this ad_id'})
  end

  rv = {:status => 'ok', :data => [IDFA_VERIFY_CONFIG[ad_id]]}
  JSON.dump(rv)
end

get '/ops_api/click/notify' do
  p params

  if params[:ad_id].nil? then
    return 404, JSON.dump({:status => 'error', :err_msg => 'params error'})
  end

  ad_id = params[:ad_id].to_i
  if !(CLICK_NOTIFY_CONFIG.keys.include? ad_id) then
    return 404, JSON.dump(
             {:status => 'error', :err_msg => 'cannot find this ad_id'})
  end

  rv = {:status => 'ok', :data => [CLICK_NOTIFY_CONFIG[ad_id]]}
  JSON.dump(rv)
end
