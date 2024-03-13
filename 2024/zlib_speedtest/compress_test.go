package main

import (
	"fmt"
	"testing"
)

func Benchmark_Compress(b *testing.B) {
	for level := 1; level <= 9; level++ {
		b.Run(fmt.Sprintf("level=%d", level), func(b *testing.B) {
			for i := 0; i < b.N; i++ {
				compress(query, level)
			}
		})
	}
}
