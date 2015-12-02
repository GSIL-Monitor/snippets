module Q02
(
 myButLast
)
where

myButLast :: [t] -> t
myButLast [] = error "cannot call myButLast on an empty list!"
myButLast [x] = error "calling myButLast on an single value list is just non-sense"
myButLast [x, y] = x
myButLast (_:xs) = myButLast xs
