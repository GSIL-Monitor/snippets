package main

import (
	"crypto/sha1"
	// "encoding/hex"
	"fmt"
	"io/ioutil"
	"os"
)

func main() {

	b, err := ioutil.ReadAll(os.Stdin)

	if err != nil {
		panic(err)
	}

	fmt.Println("got input:", string(b))

	sum := sha1.Sum(b)
	// hash_string := hex.EncodeToString(sum[:])
	// fmt.Println("hash_string:", hash_string)
	fmt.Printf("format: % x\n", sum)
	fmt.Printf("format: %x\n", sum)
}
