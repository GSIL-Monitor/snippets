package main

import "fmt";
import "os";

func main() {
	prog := os.Args[0];
	argsWithoutProg := os.Args[1:];

	if (len(os.Args) == 1) {
		fmt.Printf("%s <arguments>\n", prog);
		return;
	}

	fmt.Printf("prog: %s\n", prog);
	fmt.Printf("args: %s\n", argsWithoutProg);
}
