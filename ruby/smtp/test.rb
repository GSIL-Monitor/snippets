require 'net/smtp'
require 'pp'

smtp = Net::SMTP.new('smtp.exmail.qq.com', 465)
smtp.enable_tls
username = 'chen.lei@qianka.com'
password = '8874yumemi'

begin
  smtp.start('localhost', username, password) do |s|
    p s
    sleep(10)
  end
rescue Exception => e
  pp e.message.split(' ').first.to_i
end

sleep(10)
