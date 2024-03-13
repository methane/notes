package main

import (
	"bytes"
	"compress/zlib"
	"fmt"
	"io"
	"os"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

var query []byte

func init() {
	f, err := os.Open("world.sql")
	must(err)
	query, err = io.ReadAll(f)
	f.Close()
	must(err)
}

func compress(in []byte, level int) []byte {
	buf := bytes.NewBuffer(nil)
	w, err := zlib.NewWriterLevel(buf, level)
	must(err)
	w.Write(in)
	w.Close()
	return buf.Bytes()
}

func main() {
	fmt.Printf("query length=%d\n\n", len(query))

	fmt.Println("level, compressed, ratio")
	for level := 1; level <= 9; level++ {
		data := compress(query, level)
		fmt.Printf("%5d, %10d, %.3f\n", level, len(data), float64(len(data))/float64(len(query)))
	}

	// Determining the minimum length to compress
	idx := bytes.Index(query, []byte("INSERT INTO"))
	if idx < 0 {
		panic("INSERT INTO not found")
	}
	buff := query[idx:]
	fmt.Println("\nComparing compression ratio by size, with level=2")
	fmt.Println("uncmp len, cmp len, ratio")
	for l := 50; l < len(buff) && l < 500; l += 50 {
		data := compress(buff[:l], 2)
		fmt.Printf("%9d, %7d, %.3f\n", l, len(data), float64(len(data))/float64(l))
	}
}
