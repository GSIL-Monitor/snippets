package main

import (
	"log"
	"os"
	"regexp"
)

func main() {

	if len(os.Args) == 1 {
		log.Println("usage: regexp <exp>")
		os.Exit(1)
	}

	m, err := regexp.MatchString(`https?://.+`, os.Args[1])

	if err != nil {
		panic(err)
	}

	log.Println(m)

}
