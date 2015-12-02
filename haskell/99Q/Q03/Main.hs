import Q03

main :: IO()
main = do
  putStrLn ("the 1st element of [1,2,3] is " ++ show (elementAt [1,2,3] 1))
  putStrLn ("the 5th element of \"haskell\" is " ++ show (elementAt "haskell" 5))
