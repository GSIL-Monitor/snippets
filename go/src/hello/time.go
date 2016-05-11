package main

import "fmt"
import "time"

func main() {
	t1 := time.Now()
	t2 := time.Now()

	fmt.Printf("%T, %+v\n", t1, t1)
	fmt.Printf("%T, %+v\n", t2.Sub(t1), t2.Sub(t1))
	fmt.Println(time.Now().Format("2006-01-02"))
	t, _ := time.Parse("2006-01-02", "2016-05-11")

	l, _ := time.LoadLocation("Asia/Shanghai")

	fmt.Println(t.In(l))

}
