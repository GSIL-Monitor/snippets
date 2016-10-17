class A
  class << self
    attr_accessor :prop

    def set_prop(value)
      self.prop = value
    end
  end

  def get_prop
    return self.class.prop
  end
end

class B < A
  set_prop 'b'
end

class C < A
  set_prop 'c'
end

p B.prop
p C.prop
p B.new().get_prop
p C.new().get_prop




AMQPConsumer()\
  .connection('url')\
  .exchange('ex')\
  .queue('q')\
  .on_message(func)\
  .on_error(func)\
  .start()
