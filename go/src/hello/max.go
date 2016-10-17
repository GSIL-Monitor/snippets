package main

import "runtime"
import "log"

func main() {
	log.Println(runtime.GOMAXPROCS(100))
}
