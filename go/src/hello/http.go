package main

import (
	"fmt"
	"net/http"
	"time"
)

/*
var urls = []string{
	"http://127.0.0.1/proxy.pac",
	"http://192.168.1.234",
	"http://172.20.1.10/",
}
*/

var urls = []string{
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
	"http://127.0.0.1:4567/sleep",
}

type HttpResponse struct {
	url string
	response *http.Response
	err error
}

func asyncHttpGets(urls []string) []*HttpResponse {
	ch := make(chan *HttpResponse)
	responses := []*HttpResponse{}
	client := http.Client{}
	for _, url := range urls {
		go func (url string) {
			fmt.Printf("Fetching %s\n", url);
			resp, err := client.Get(url)
			ch <- &HttpResponse{url, resp, err}
			if err != nil && resp != nil &&
				resp.StatusCode == http.StatusOK {
				resp.Body.Close()
			}
		}(url)
	}

	for {
		select {
		case r := <- ch:
			fmt.Printf("%s was fetched\n", r.url)
			if r.err != nil {
				fmt.Println("with an error", r.err)
			}
			responses = append(responses, r)
			if len(responses) == len(urls) {
				return responses
			}
		case <- time.After(50 * time.Millisecond):
			fmt.Printf(".")
		}
	}

}

func main() {
	for {
		asyncHttpGets(urls)
	}
}
