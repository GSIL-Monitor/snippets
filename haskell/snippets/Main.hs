module Main where

import qualified Database.Redis as Redis
import Data.String (fromString)
import Control.Monad.IO.Class (liftIO)


connInfo :: Redis.ConnectInfo
connInfo = Redis.defaultConnectInfo {
             Redis.connectHost = "127.0.0.1"
           , Redis.connectPort = Redis.PortNumber 6380
           }


inspectLength x = do
  conn <- Redis.connect connInfo
  Redis.runRedis conn $ do
                    k <- Redis.scard x
                    case k of
                      Left e -> error "redis error"
                      Right result -> result



main :: IO ()
main = do
  conn <- Redis.connect connInfo
  Redis.runRedis conn $ do
         k <- Redis.keys (fromString "qianka:eeyore:app_idfas*")
         case k of
           Left e -> error "redis error"
           Right result -> do
                          liftIO $ print (map inspectLength result)
