package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	target := flag.String("target", "localhost:7000", "target to proxy")
	flag.Parse()

	conn, err := net.Dial("udp", *target)
	must(err)
	defer conn.Close()
	fmt.Printf("connected to %s from %s\n", conn.RemoteAddr(), conn.LocalAddr())

	uconn := conn.(*net.UDPConn)

	msg0 := strings.Repeat(fmt.Sprintf("hello, from %d. ", os.Getpid()), 1000)
	buff := make([]byte, 4000)

	for i := 100; i < 4000; i += 10 {
		time.Sleep(time.Second * 1)
		t0 := time.Now()
		//conn.Write(msg)
		fmt.Printf("sending %d bytes\n", i)
		n, err := conn.Write([]byte(msg0[:i]))
		fmt.Printf("sent %d bytes (err=%v)\n", n, err)

		n, addr, err := uconn.ReadFromUDP(buff)
		must(err)

		fmt.Printf("received %d bytes from %s (d=%v)\n", n, addr, time.Since(t0))
		fmt.Printf("data: %q\n", string(buff[:n]))
	}
}
