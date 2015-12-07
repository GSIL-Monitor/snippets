module Q06
(
 isPalindrome
)
where

removeFirst :: [a] -> [a]
removeFirst [] = []
removeFirst [_] = []
removeFirst (_:xs) = xs

removeLast :: [a] -> [a]
removeLast [] = []
removeLast [_] = []
removeLast (x:xs) = [x] ++ removeLast xs

getLast :: [a] -> a
getLast [] = error "cannot get last element of an empty list"
getLast [x] = x
getLast (_:xs) = getLast xs

isPalindrome :: Eq a => [a] -> Bool
isPalindrome [] = True
isPalindrome [_] = True
isPalindrome x = (head x == getLast x) && isPalindrome (removeFirst (removeLast x))
