require 'bigdecimal'


CPU_PATTERN = /collectd\.(?<hostname>.+)\.cpu-.*\.cpu-(?<item>.+)/

class CPU

  attr_accessor :core_num, :user, :sys, :idle, :wait, :steal

  def initialize()
    @core_num = 0
    @user = BigDecimal.new("0")
    @sys = BigDecimal.new("0")
    @idle = BigDecimal.new("0")
    @wait = BigDecimal.new("0")
    @steal = BigDecimal.new("0")
  end

  def total_usage
    # @user + @sys + @idle + @wait + @steal / @core_num
    sprintf("%.1f%%", ((@user + @sys + @wait + @steal) / @core_num))
  end

  def user_usage
    # @user + @sys + @idle + @wait + @steal / @core_num
    sprintf("%.1f%%", (@user / @core_num))
  end


  def sys_usage
    # @user + @sys + @idle + @wait + @steal / @core_num
    sprintf("%.1f%%", (@sys / @core_num))
  end


  def idle_usage
    # @user + @sys + @idle + @wait + @steal / @core_num
    sprintf("%.1f%%", (@idle / @core_num))
  end


  def wait_usage
    # @user + @sys + @idle + @wait + @steal / @core_num
    sprintf("%.1f%%", (@wait / @core_num))
  end


  def steal_usage
    # @user + @sys + @idle + @wait + @steal / @core_num
    sprintf("%.1f%%", (@steal / @core_num))
  end


end

def get_cpu_info(hostname)

  hosts = {}

  data = graphite_fetch_data(
    hostname,
    'collectd.h*.cpu-*.cpu-user'
  )

  data.each do |line|
    m = CPU_PATTERN.match(line['target'])
    unless m.nil?
      unless hosts.include? m['hostname']
        hosts[m['hostname']] = CPU.new
      end
      hosts[m['hostname']].core_num += 1
    end
  end

  data = graphite_fetch_data(
    hostname,
    'collectd.h*.cpu-*.cpu-*'
  )


  data.each do |line|
    m = CPU_PATTERN.match(line['target'])
    unless m.nil?
      if m['item'] == 'user'
        hosts[m['hostname']].user +=
          BigDecimal.new(line['datapoints'].first.first.to_s)
      end
      if m['item'] == 'sys'
        hosts[m['hostname']].sys +=
          BigDecimal.new(line['datapoints'].first.first.to_s)
      end
      if m['item'] == 'idle'
        hosts[m['hostname']].idle +=
          BigDecimal.new(line['datapoints'].first.first.to_s)
      end
      if m['item'] == 'wait'
        hosts[m['hostname']].wait +=
          BigDecimal.new(line['datapoints'].first.first.to_s)
      end
      if m['item'] == 'steal'
        hosts[m['hostname']].steal +=
          BigDecimal.new(line['datapoints'].first.first.to_s)
      end

    end
  end

  hosts

end
