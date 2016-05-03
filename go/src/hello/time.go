package main;

import "fmt";
import "time";

func main () {
	t1 := time.Now();
	t2 := time.Now();

	fmt.Println(t2.Sub(t1));
}
