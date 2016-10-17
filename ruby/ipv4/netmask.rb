ip_with_mask = ARGV.shift

ip, mask = ip_with_mask.split('/')

def ip_to_arr(ip)
  arr = ip.split('.')
  arr.map{|x|x.to_i}
end

def mask_to_arr(mask)
  full_mask = ("1" * 32).to_i(2)
  mask_complement = ("1" * (32 - mask.to_i)).to_i(2)
  mask_binary = (full_mask ^ mask_complement).to_s(2)
  mask_binary.scan(/.{8}/).map{|x|x.to_i(2)}
end

def mask_ip(mask, ip)
  mask.zip(ip).map{|x| x[0] & x[1]}
end

ip = ip_to_arr(ip)
mask = mask_to_arr(mask)
_ = mask_ip(mask, ip)
network = _.map{|x|x.to_s}.join('.')
netmask = mask.map{|x|x.to_s}.join('.')
print("#{network} #{netmask}\n")
