package main

import "flag"
import "log"

var config_file = flag.String("config", "eeyore.toml", "config file")

func main() {
	flag.Parse()
	log.Println(*config_file)
}
