result = {}

for i = 1,10000 do
  i = math.random(3)
  if result[i] == nil then
    result[i] = 1
  else
    result[i] = result[i] + 1
  end
end

for k, v in pairs(result) do
  print(k, v)
end
