import Q05

main :: IO()
main = do
  putStrLn ("the reverse of \"A man, a plan, a canal, panama!\" is " ++ show (myReverse "A man, a plan, a canal, panama!"))
  putStrLn ("the reverse of [1,2,3,4] is " ++ show (myReverse [1,2,3,4]))
