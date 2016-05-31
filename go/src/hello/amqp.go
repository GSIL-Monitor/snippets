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

	err = ch.Qos(3, 0, false)
	handleError(err)

	msgs, err := ch.Consume(
		q.Name,
		"",    // consumer
		false, // auto-ack
		false, // exclusive
		false, // no-local
		false, // no-wait
		nil,   // args
	)
	handleError(err)

	log.Printf("%T", msgs)
	log.Printf("%+v", msgs)

	forever := make(chan bool)

	worker := func() {
		for d := range msgs {
			d.Ack(true)
			// log.Printf("%+v", d)
			// log.Printf("%T", d)
			// log.Printf("received: %s", d.Body)
		}
	}

	go worker()

	log.Printf(" [*] waiting for messages incoming")

	<-forever
}
