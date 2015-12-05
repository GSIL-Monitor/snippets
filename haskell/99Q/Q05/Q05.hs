module Q05
(
 myReverse
)

where

myReverse :: [t] -> [t]
myReverse [] = []
myReverse (x:xs) = (myReverse xs) ++ [x]
