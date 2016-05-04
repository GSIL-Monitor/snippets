package main

import (
  "fmt"
  "net/url"
)

func main () {
  u := new(url.URL)
  q := u.Query()
  q.Add("q", "golang")
  q.Add("q", "python")
  fmt.Println(q.Encode())
}
