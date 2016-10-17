require 'addressable/uri'
require 'unirest'



def graphite_fetch_data(hostname, target, from='-1min')

  u = Addressable::URI.new
  u.host = hostname
  u.scheme = 'http'
  u.path = 'render'
  u.query_values = {
    :target => target,
    :format => 'json',
    :from => from,
    :util => 'now',
  }

  url = u.to_s

  res = Unirest.get url

  if res.code != 200
    raise RuntimeError.new "response status not 200!"
  end

  res.body

end
