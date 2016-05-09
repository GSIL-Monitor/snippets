package main

import (
	"github.com/streadway/amqp"
	"log"
)

func handleError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@127.0.0.1:5672/")
	handleError(err)
	defer conn.Close()

	ch, err := conn.Channel()
	handleError(err)
	defer ch.Close()

	/*
		log.Printf(" [x] Sent %s", body)
		handleError(err)
	*/

	q, err := ch.QueueDeclare(
		"test", // name
		false,  // durable
		true,   // auto-delete
		false,  //exclusive
		false,  // no-wait
		nil,    // arguments
	)
	handleError(err)

	err = ch.QueueBind(
		q.Name,
		"*",         // routing key
		"amq.topic", // exchange,
		false,
		nil,
	)
	handleError(err)

	msgs, err := ch.Consume(
		q.Name,
		"",    // consumer
		true,  // auto-ack
		false, // exclusive
		false, // no-local
		false, // no-wait
		nil,   // args
	)
	handleError(err)

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			log.Printf("received: %s", d.Body)
		}
	}()

	log.Printf(" [*] waiting for messages incoming")

	<-forever
}
