package main

import "log"
import "flag"
import "github.com/garyburd/redigo/redis"
import "time"

var (
	pool        *redis.Pool
	redisServer = flag.String("redisServer", ":6379", "")
)

func newPool(server string) *redis.Pool {
	return &redis.Pool{
		MaxActive:   100,
		MaxIdle:     3,
		IdleTimeout: 10 * time.Second,
		Dial: func() (redis.Conn, error) {
			c, err := redis.Dial("tcp", server)
			if err != nil {
				return nil, err
			}
			/*
				if _, err := c.Do("AUTH", ""); err != nil {
					c.Close()
					return nil, err
				}
			*/
			return c, err
		},
		TestOnBorrow: func(c redis.Conn, t time.Time) error {
			_, err := c.Do("PING")
			return err
		},
	}
}

func get(id int, q chan bool) {
	conn := pool.Get()
	defer conn.Close()
	for {
		v := <-q
		if v {

			_, err := conn.Do("SET", "hello", 10)

			res, err := conn.Do(
				"GET", "hello")
			if err != nil {
				log.Println(err)
				return
			}
			if res != nil {
				log.Printf("%T", res)
				log.Printf("%+v", res)
				log.Printf("%+v", string(res.([]byte)))
			}
		}
	}
}

func main() {
	flag.Parse()
	pool = newPool(*redisServer)

	q := make(chan bool)

	for i := 0; i < 10; i++ {
		go get(i, q)
	}

	for {
		q <- true
	}
}
