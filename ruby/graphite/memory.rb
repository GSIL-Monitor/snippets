MEMORY_PATTERN = /collectd\.(?<hostname>.+)\.memory\.memory-(?<item>.+)/

class Memory

  attr_accessor :used, :free, :buffered, :cached, :used_per, :free_per

  def initialize(used=0, free=0, buffered=0, cached=0)
    @used = used
    @free = free
    @buffered = buffered
    @cached = cached
  end

  def total
    @used + @free + @buffered + @cached
  end

  def used_per
    if total.to_f == 0.0
      return "N/A"
    end

    sprintf("%.1f%%", (@used / total) * 100)
  end

  def real_free
    @free + @buffered + @cached
  end

  def free_per
    if total.to_f == 0.0
      return "N/A"
    end

    sprintf("%.1f%%", (real_free / total) * 100)
  end

end


def get_memory_info(hostname)

  hosts = {}

  data = graphite_fetch_data(
    hostname,
    'collectd.h*.memory.memory-{free,used,cached,buffered}'
  )

  data.each do |line|
    m = MEMORY_PATTERN.match(line['target'])
    unless m.nil?
      unless hosts.include? m['hostname']
        hosts[m['hostname']] = Memory.new
      end

      if m['item'] == 'used'
        hosts[m['hostname']].used = line['datapoints'].first.first
      end
      if m['item'] == 'free'
        hosts[m['hostname']].free = line['datapoints'].first.first
      end
      if m['item'] == 'buffered'
        hosts[m['hostname']].buffered = line['datapoints'].first.first
      end
      if m['item'] == 'cached'
        hosts[m['hostname']].cached = line['datapoints'].first.first
      end
    end
  end

  hosts

end
