plusOne :: Int -> Int
plusOne x = x + 1

addition :: Int -> Int -> Int
addition x 0 = x
addition x 1 = plusOne x
addition x y = addition (plusOne x) (y - 1)
