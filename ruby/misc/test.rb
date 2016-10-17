def npercentile data, n
  data.sort!
  idx = (data.length * n / 100).to_i

  return data[idx - 1]
end
