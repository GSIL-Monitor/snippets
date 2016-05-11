package main

import "log"
import "time"

func main() {

	var m []time.Time

	t1 := time.Now()
	for i := 0; i < 10000000; i++ {
		m = append(m, time.Now())
	}
	t2 := time.Now()

	cnt := 0
	for _, t := range m {
		if t2.Sub(t) < time.Second*10 {
			cnt++
		}
	}

	log.Println(cnt)
	log.Println(t2.Sub(t1))
}
