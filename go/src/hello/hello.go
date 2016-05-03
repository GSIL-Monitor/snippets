package main

import (
	"fmt"
)


func feed(ch chan string, payload string) {
	ch <- payload
}

func r(msg string) {
	fmt.Println(msg)
}

func main() {

	// runtime.GOMAXPROCS(1)

	messages := make(chan string)

	go feed(messages, "ping")

	for {
		select {
		case c := <- messages:
			go r(c)
			go feed(messages, "ping")
		}
	}
}
