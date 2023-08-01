package main

import (
	"flag"
	"fmt"
	"net"
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

	for {
		time.Sleep(time.Second * 3)
		conn.Write([]byte("hello"))

		buff := make([]byte, 100)
		n, addr, err := uconn.ReadFromUDP(buff)
		must(err)

		fmt.Printf("received %d bytes from %s\n", n, addr)
		fmt.Printf("data: %q\n", string(buff[:n]))
	}
}
