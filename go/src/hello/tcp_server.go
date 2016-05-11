package main

import (
	"tcp_server"
)

func main() {

	add := []string{"127.0.0.1:9999", "127.0.0.1:9998"}

	server := tcp_server.New(add)

	server.OnNewClient(func(c *tcp_server.Client) {
		c.Send("hello")
	})

	server.OnNewMessage(func(c *tcp_server.Client, message string) {
		c.Send(message)
	})

	server.Listen()
}
