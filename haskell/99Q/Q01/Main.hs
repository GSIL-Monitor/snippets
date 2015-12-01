import Q01

main :: IO()
main = do
  putStrLn ("The last element of [1,2,3,4] is " ++ show (myLast [1,2,3,4]))
  putStrLn ("The last element of ['x', 'y', 'z'] is " ++ show (myLast ['x', 'y', 'z']))
