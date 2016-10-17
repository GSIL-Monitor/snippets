factorial :: Int -> Int
factorial x
  | x == 0     = 1
  | x > 0      = x * factorial (x - 1)
  | otherwise  = error "num should be positive"
