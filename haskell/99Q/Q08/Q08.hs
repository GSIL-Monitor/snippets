module Q08 where

removeFirst :: [a] -> [a]
removeFirst [] = []
removeFirst [_] = []
removeFirst (_:xs) = xs

compress :: Eq a => [a] -> [a]
compress [] = []
compress [x] = [x]
compress (x:xs) = do
  if x == (head xs)
  then compress ([x] ++ (removeFirst xs))
       else [x] ++ compress(xs)
