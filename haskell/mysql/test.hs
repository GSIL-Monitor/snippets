import Database.MySQL.Simple (connect, defaultConnectInfo, query)

main :: IO ()
main = putStrLn hello

hello = do
  conn <- connect defaultConnectInfo
  query conn "SELECT 2 + 2"
