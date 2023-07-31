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
	host := flag.String("host", "localhost", "host to connect")
	port := flag.Int("port", 7000, "port to connect")
	flag.Parse()

	conn, err := net.Dial("udp", fmt.Sprintf("%s:%d", *host, *port))
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
