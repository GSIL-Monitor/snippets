power :: Int -> Int -> Int
power _ 0 = 1
power x 1 = x
power x y = x * power x (y - 1)
