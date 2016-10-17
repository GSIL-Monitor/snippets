require 'eventmachine'




class RandomWords < EventMachine::Connection
  def post_init
    puts "connection made"

    while true
      send_data 'hello'
    end

  end
end


EventMachine.run {
  EventMachine.start_server "127.0.0.1", 9000, RandomWords
}
