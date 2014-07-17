package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"
)

func main() {

	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "invalid argument. use a fraction to sample between 0.0 (no sampling) and 1.0 (100% sampling)")
		os.Exit(1)
	}

	target, err := strconv.ParseFloat(os.Args[1], 64)
	if err != nil || target < 0.0 || target > 1.0 {
		fmt.Fprintf(os.Stderr, "Unable to convert %q to a float between 0.0 and 1.0", os.Args[1])
		os.Exit(1)
	}

	rand.Seed(time.Now().UnixNano())
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		if target < rand.Float64() {
			continue
		}
		fmt.Printf("%q", scanner.Text()) // Println will add back the final '\n'
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
		os.Exit(2)
	}
}
