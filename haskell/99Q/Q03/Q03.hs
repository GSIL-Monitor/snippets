module Q03
(
 elementAt
)
where

elementAt [] _    = error "cannot find any element in an empty list!"
elementAt _ 0     = error "0 is not a valid index!"
elementAt (x:_) 1 = x
elementAt (_:xs) y
    | y < 1       = error "index should be greater than 1"
    | otherwise   = elementAt xs (y-1)
