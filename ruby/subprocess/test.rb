require 'json'
def run_in_child(cmd)
  command = %Q(/bin/bash -l -c "#{cmd}")
  read, write = IO.pipe
  Process.fork do
    $stdout.reopen(write)
    $stderr.reopen(write)
    exec command
  end
  write.close
  Process.wait
  p $?.exitstatus
  p $?.success?
  _ = read.read
  read.close
  return $?, _
end

python_binary = 'local/bin/python'
hostname = 'n1386.ops.gaoshou.me'

cmd = "#{python_binary} test.py --hostname #{hostname} --task test"

rv = run_in_child(cmd)
# print rv
reg = /--------PLOCEUS RUBY RESULT START--------(.+)--------PLOCEUS RUBY RESULT END--------/m
result = JSON.parse(reg.match(rv[1])[1].strip)

p result[hostname]
