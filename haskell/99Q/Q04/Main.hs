import Q04

main :: IO()
main = do
  putStrLn ("length of [123, 456, 789] is " ++ show (myLength [123, 456, 789]))
  putStrLn ("length of \"Hello, world!\" is " ++ show (myLength "Hello world!"))
