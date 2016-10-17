package main

import (
	"fmt"
	"log"
	"net"
	"strconv"
	"time"
)

type StatClient struct {
	Endpoint string

	conn net.Conn
}

func (client *StatClient) Send(payload string) {
	client.connect()
	fmt.Fprintf(client.conn, payload)
}

func (client *StatClient) connect() {
	if client.conn != nil {
		return
	}
	conn, err := net.Dial("udp", client.Endpoint)
	if err != nil {
		log.Println(err)
		return
	}
	client.conn = conn
}

func main() {
	client := StatClient{
		Endpoint: "127.0.0.1:4000",
	}

	for i := 0; i < 10000; i++ {

		// log.Printf("%T", conn)

		client.Send(strconv.FormatInt(time.Now().Unix(), 10))
		// conn.Close()
	}
}
