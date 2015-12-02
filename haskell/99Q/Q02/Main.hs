import Q02

main :: IO()
main = do
  putStrLn ("The last but one element of [1,2,3,4] is " ++ show (myButLast [1,2,3,4]))
  putStrLn ("The last but one element of ['a'..'z'] is " ++ show (myButLast ['a'..'z']))
