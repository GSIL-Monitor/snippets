import Q06

main :: IO()
main = do
  putStrLn ("[1,2,3] is a palindrome ? " ++ (show (isPalindrome [1,2,3])))
  putStrLn ("\"madamimadam\" is a palindrome ? " ++ (show (isPalindrome "madamimadam")))
  putStrLn ("[1,2,4,8,16,8,4,2,1] is a palindrome ? " ++ (show (isPalindrome [1,2,4,8,16,8,4,2,1])))
