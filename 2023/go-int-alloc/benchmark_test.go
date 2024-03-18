// go-mysql-driverでtext protocolの時にintをintとしてanyに格納しても
// アロケーションが増えないことを確認する。

package main

import (
	"strconv"
	"testing"
)

var x []byte = []byte("114514")

//go:noinline
func readAsBytes() []interface{} {
	res := make([]interface{}, 8)
	for i := 0; i < 8; i++ {
		res[i] = x
	}
	return res
}

//go:noinline
func readAsInt() []interface{} {
	res := make([]interface{}, 8)
	for i := 0; i < 8; i++ {
		res[i], _ = strconv.ParseInt(string(x), 10, 64)
	}
	return res
}

func Benchmark_Bytes(b *testing.B) {
	for i := 0; i < b.N; i++ {
		readAsBytes()
	}
}

func Benchmark_Ints(b *testing.B) {
	for i := 0; i < b.N; i++ {
		readAsInt()
	}
}
