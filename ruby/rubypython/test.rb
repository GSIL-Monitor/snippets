require 'rubypython'

RubyPython.start_from_virtualenv('local')

test2 = RubyPython.import('test2')
api = RubyPython.import('ploceus.api')

hostname = 'n1386.ops.gaoshou.me'
_ = api.run_task(test2.test, [hostname], hello: 'test')
if _.include? hostname then
  result = _[hostname]
  p result.rv
  print result.rv
end
