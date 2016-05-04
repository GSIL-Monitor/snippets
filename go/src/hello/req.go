package main

import (
  "bytes"
  "fmt"
  "io/ioutil"
  "net/http"
  "net/url"
  "time"
)


func sendReq (r string) {
  u := new(url.URL)
  q := u.Query()
  q.Add("lang", "golang")
  url := "http://127.0.0.1:4567/put"
  req, err := http.NewRequest("PUT", url, bytes.NewBuffer([]byte(q.Encode())))
  req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
  client := &http.Client{}
  resp, err := client.Do(req)
  if err != nil {
    panic(err)
  }


  defer resp.Body.Close()

  fmt.Println("status:", resp.Status)
  fmt.Println("headers:", resp.Header)

  body, _ := ioutil.ReadAll(resp.Body)
  fmt.Println("body:", string(body))
}

func feed(ch chan string, payload string) {
  ch <- payload
}

func main () {

  fmt.Println("1")
  p := make(chan string)
  fmt.Println("2")

  for i := 0; i < 5; i++ {
    go feed(p, "a")
  }

  for {
    select {
    case r := <- p:
      go sendReq(r)
    case <- time.After(50 * time.Millisecond):
      fmt.Printf(".")
    }
  }

}
