package test_escape

import (
	"testing"
)

func escape0(buf []byte, s string) []byte {
	pos := 0

	for _, c := range []byte(s) {
		switch c {
		case '\\':
			buf[pos] = '\\'
			buf[pos+1] = '\\'
			pos += 2
		case '\n':
			buf[pos] = '\\'
			buf[pos+1] = 'n'
			pos += 2
		default:
			buf[pos] = c
			pos++
		}
	}

	return buf[:pos]
}

func escape1(buf []byte, s string) []byte {
	pos := 0

	for _, c := range []byte(s) {
		switch c {
		case '\\':
			buf[pos+1] = '\\'
			buf[pos] = '\\'
			pos += 2
		case '\n':
			buf[pos+1] = 'n'
			buf[pos] = '\\'
			pos += 2
		default:
			buf[pos] = c
			pos++
		}
	}

	return buf[:pos]
}

func escape2(buf []byte, s string) []byte {
	pos := 0
	cnt := 0

	for i, c := range []byte(s) {
		switch c {
		case '\\':
			copy(buf[pos:pos+cnt], s[i-cnt:i])
			pos += cnt
			cnt = 0
			buf[pos+1] = '\\'
			buf[pos] = '\\'
			pos += 2
		case '\n':
			copy(buf[pos:pos+cnt], s[i-cnt:i])
			pos += cnt
			cnt = 0
			buf[pos+1] = 'n'
			buf[pos] = '\\'
			pos += 2
		default:
			cnt++
		}
	}
	copy(buf[pos:pos+cnt], s[len(s)-cnt:])
	return buf[:pos+cnt]
}

var message = "abcdefghijkl\nmnopqrstuvwxyz012345\\abcdefghijkl"

func BenchmarkEscape0(b *testing.B) {
	buf := make([]byte, len(message)*2)
	for i := 0; i < b.N; i++ {
		escape0(buf, message)
	}
}

func BenchmarkEscape1(b *testing.B) {
	buf := make([]byte, len(message)*2)
	for i := 0; i < b.N; i++ {
		escape1(buf, message)
	}
}

func BenchmarkEscape2(b *testing.B) {
	buf := make([]byte, len(message)*2)
	for i := 0; i < b.N; i++ {
		escape2(buf, message)
	}
}
