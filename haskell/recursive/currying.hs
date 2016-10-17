multiplyList :: Int -> [Int] -> [Int]
multiplyList _ [] = []
multiplyList x (n:ns) = (x * n) : (multiplyList x ns)

doubleList :: [Int] -> [Int]
doubleList x = multiplyList 2 x
