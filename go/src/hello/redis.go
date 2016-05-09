package main

import "fmt"
import "time"
import "gopkg.in/redis.v3"


func main() {
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
		Password: "",
		DB: 0,
	});

  d := time.Second * 1

	pong, err := client.BLPop(d, "test").Result()

	if err != redis.Nil && err != nil {
    fmt.Printf("err: %v\n", err)
    fmt.Printf("err: %T\n", err)
	} else {
		fmt.Printf("result: %v\n", pong)
	}

}
