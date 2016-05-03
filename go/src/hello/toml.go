package main

import (
	"fmt"
  "io/ioutil"
  "os"
	"github.com/BurntSushi/toml"
)


type Config struct {
  Debug bool
  Databases map[string]Database
}

type Database struct {
  Host string
  Port int
  User string
  Pass string
  Dbname string
}

func main() {

  var config Config

	prog := os.Args[0]
	if (len(os.Args) == 1) {
		fmt.Printf("%s <arguments>\n", prog);
		return
	}

	f := os.Args[1]
  fmt.Println("reading", f)

  tomlData, err := ioutil.ReadFile(f)

  _, err = toml.Decode(string(tomlData), &config)
  if err != nil {
    fmt.Println("toml decode error!")
    return
  }

  fmt.Printf("Debug: %v\n", config.Debug)
  fmt.Printf("Debug: %v\n", config.Databases)
  for k := range config.Databases {
    fmt.Println("=== new database ===")
    fmt.Printf("Key: %v\n", k)
    fmt.Printf("Host: %v\n", config.Databases[k].Host)
    fmt.Printf("Port: %v\n", config.Databases[k].Port)
    fmt.Printf("User: %v\n", config.Databases[k].User)
    fmt.Printf("Pass: %v\n", config.Databases[k].Pass)
    fmt.Printf("Dbname: %v\n", config.Databases[k].Dbname)
  }
}
