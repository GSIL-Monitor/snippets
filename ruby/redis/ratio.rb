#!/usr/bin/env ruby

hits_ = nil
misses_ = nil

loop do
  `redis-cli -h n1498.ops.gaoshou.me -p 6379 info | grep keyspace` =~ /hits:(\d+).*misses:(\d+)/m
  hits, misses = $1.to_i, $2.to_i

  if hits_
    dhits = hits - hits_
    dmisses = misses - misses_

    puts "%s: %.02f%% (%d / %d)" % [Time.now, dhits * 100.0 /
                                                   (dhits + dmisses),
                                    dhits, dhits + dmisses]
  end

  hits_ = hits
  misses_ = misses

  sleep 1
end
