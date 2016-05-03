package main

import "fmt";
import "gopkg.in/redis.v3";

func main() {
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		Password: "",
		DB: 0,
	});

	pong, err := client.Info().Result();

	fmt.Println(pong, err);
}
