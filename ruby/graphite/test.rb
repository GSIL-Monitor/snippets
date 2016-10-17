require './cpu'
require './disk'
require './graphite'
require './host'
require './memory'




if ARGV.empty?
  puts "ruby test.rb hostname"
  exit
end

hostname = ARGV.shift

# memory = get_memory_info hostname

# cpu = get_cpu_info hostname
#
# cpu.each do |k|
#   puts "#{k.first}\t#{k[1].total_usage}"
# end

disks = get_disk_info(hostname)
disks.each do |k|
  puts "#{k[0]}\t#{k[1].used_per}"
end
