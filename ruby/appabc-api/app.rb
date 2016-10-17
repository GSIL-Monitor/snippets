#!/usr/bin/env ruby
require 'json'
require 'sinatra'

get '/api/brush_list/alguns/:machine_id' do

  appid = []
  120.to_i.times do
    appid.push 'reverie.chen@gmail.com,123456,123'
  end
  appid = appid.join('||')

  rv = {
    :id => 1234,
    :name => 'test',
    :view_url => 'https://itunes.apple.com/cn/app/meng-hui-tie-jia-jian-ling/id1029821591?mt=8',
    :device_flag => nil,
    :thread_num => 24,
    :task_timeout => 2,
    :interval_switch => 1,
    :interval_time => 5,
    :appid => appid,
  }
  response.headers['Content-Type'] = 'application/json'
  return JSON.generate(rv)
end

post '/api/brush_record' do
  p params[:appid]
  p params[:fail_string]
  p params[:id]
  ''
end

post '/api/success_record' do
  p params[:appid]
  p params[:fail_error]
  p params[:id]
  ''
end

get '/api/stop/id/:task_id' do
  '1'
end
