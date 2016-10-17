require 'bigdecimal'

DISK_PATTERN = /collectd\.(?<hostname>.+)\.df-root\.df_complex-(?<item>.+)/

class Disk

  attr_accessor :name, :free, :used, :reserved

  def initialize(name)
    @name = name
    @free = BigDecimal.new("0")
    @used = BigDecimal.new("0")
  end

  def total
    @free + @reserved + @used
  end


  def used_per
    sprintf("%.1f%%", ((@used + @reserved)/ total) * 100)
  end

end


def get_disk_info(hostname)

  hosts = {}

  data = graphite_fetch_data(hostname, 'collectd.h*.df-root.*')

  data.each do |line|
    m = DISK_PATTERN.match(line['target'])

    unless m.nil?
      unless hosts.include? m['hostname']
        hosts[m['hostname']] = Disk.new('root')
      end

      if m['item'] == 'free'
        hosts[m['hostname']].free =
          BigDecimal.new line['datapoints'].first.first.to_s
      end
      if m['item'] == 'used'
        hosts[m['hostname']].used =
          BigDecimal.new line['datapoints'].first.first.to_s
      end
      if m['item'] == 'reserved'
        hosts[m['hostname']].reserved =
          BigDecimal.new line['datapoints'].first.first.to_s
      end

    end

  end

  hosts

end
