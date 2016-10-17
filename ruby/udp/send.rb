require 'fcntl'
require 'socket'
require 'time'

s = UDPSocket.new
# s.fcntl(Fcntl::F_SETFL, Fcntl::O_NONBLOCK)

while true
  s.send Time.now.to_s, 0, '127.0.0.1', 4000
end

result = IO.select([s], nil, nil, 1)

unless result.nil?
  result.first.each do |sock|
    p sock.recv(100)
  end
end
