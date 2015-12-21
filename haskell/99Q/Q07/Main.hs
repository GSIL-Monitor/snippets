{-# LANGUAGE ExtendedDefaultRules #-}

import Q07


main = do
  putStrLn ("flatten (Elem 5) => " ++ show (flatten (Elem 5)))
  putStrLn ("flatten (List [Elem 1, List \
             \[Elem 2, List [Elem 3, Elem 4]\
             \, Elem 5]]) => " ++
            show (flatten
                  (List
                   [Elem 1, List [Elem 2, List [Elem 3, Elem 4], Elem 5]])))
  putStrLn ("flatten (List []) => " ++ show (flatten (List [])))
