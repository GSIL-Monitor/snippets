require 'logger'
require 'snmp'
require 'socket'
require 'yaml'


logger = Logger.new(STDOUT)

c = YAML.load(File.read('config.yml'))
logger.info(c)

class Statsd

  attr :socket, :host, :port

  def initialize(host, port)
    @host = host
    @port = port
    @socket = UDPSocket.new
  end

  def send(message)
    @socket.send(message, 0, @host, @port)
  end

  def destroy
    @socket.close
  end

end

class SNMPHelper

  attr :manager

  def initialize(host)
    @manager = SNMP::Manager.new(:host => host)
  end

  def destroy
    @manager.close
  end

  def get_in_octects(if_oid)
    oid = "1.3.6.1.2.1.2.2.1.10.#{if_oid}"
    resp = manager.get(oid)
    return resp.varbind_list.first.value.to_i
  end

  def get_out_octects(if_oid)
    oid = "1.3.6.1.2.1.2.2.1.16.#{if_oid}"
    resp = manager.get(oid)
    return resp.varbind_list.first.value.to_i
  end

  def get_cpu_usage
    oid = "1.3.6.1.4.1.25506.2.6.1.1.1.1.6.3"
    resp = manager.get(oid)
    return resp.varbind_list.first.value.to_i
  end

  def get_mem_usage
    oid = "1.3.6.1.4.1.25506.2.6.1.1.1.1.8.3"
    resp = manager.get(oid)
    return resp.varbind_list.first.value.to_i
  end

end

def monitor(c)
  s = Statsd.new(c["statsd"]["host"], c["statsd"]["port"])
  h = SNMPHelper.new(c["host"])

  c["interfaces"].each do |k, v|
    i = h.get_in_octects(v)
    m = "job.ops.office.er8300g2.#{k}.inOctets:#{i}|g"
    s.send(m)

    o = h.get_out_octects(v)
    m = "job.ops.office.er8300g2.#{k}.outOctets:#{o}|g"
    s.send(m)
  end

  cpu = h.get_cpu_usage
  m = "job.ops.office.er8300g2.cpu:#{cpu}|g"
  s.send(m)

  mem = h.get_mem_usage
  m = "job.ops.office.er8300g2.memory:#{mem}|g"
  s.send(m)

  h.destroy
  s.destroy
end

while (true)
  thr = Thread.new { monitor(c) }
  thr.join
  sleep(c["interval"])
end
