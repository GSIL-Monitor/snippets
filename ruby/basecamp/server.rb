require 'eventmachine'

require 'active_record'

config = {
    'adapter' => 'sqlite3',
    'database' => '/tmp/test.sqlite3'
}

ActiveRecord::Base.establish_connection(config)

__END__

class UDPHandler < EventMachine::Connection
  def receive_data data
    puts data.chomp
    send_data(data)
    send_data(data)
  end

end

EventMachine.run do
  EventMachine.open_datagram_socket('0.0.0.0', 9000, UDPHandler)
end
