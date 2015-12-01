module Q01
(myLast) where

myLast :: [a] -> a
myLast [] = error "can't call myLast on an empty list!"
myLast [x] = x
myLast (_:xs) = myLast xs
