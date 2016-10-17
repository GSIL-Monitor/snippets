myreplicate :: Int -> a -> [a]
myreplicate 0 _ = []
myreplicate x a = a : (myreplicate (x - 1))
