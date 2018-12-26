import Q01

import System.Environment (getArgs)

-- main :: IO()
-- main = do
--   putStrLn ("The last element of [1,2,3,4] is " ++ show (myLast [1,2,3,4]))
--   putStrLn ("The last element of ['x', 'y', 'z'] is " ++ show (myLast ['x', 'y', 'z']))

main :: IO()
main = do
  (action:_) <- getArgs; print action
