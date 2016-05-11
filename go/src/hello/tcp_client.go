package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {

	// connect to this socket
	conn, _ := net.Dial("tcp", "127.0.0.1:9999")
	for {
		// send to socket
		fmt.Fprintf(conn, "hello\n")
		// listen for reply
		message, _ := bufio.NewReader(conn).ReadString('\n')
		fmt.Print("Message from server: " + message)
	}
}
