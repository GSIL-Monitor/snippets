require 'date'

Date.new(2018, 10, 9).upto(Date.new(2018, 10, 18)).each do |d|
  tn = d.strftime('user_app_status_%Y%m%d')
  print("TRUNCATE TABLE #{tn};\n")
  print("OPTIMIZE TABLE #{tn};\n")
end
