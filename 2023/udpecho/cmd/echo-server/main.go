package main

import (
	"flag"
	"fmt"
	"net"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	port := flag.Int("port", 7000, "port to listen")
	flag.Parse()

	fmt.Printf("listening on port %d\n", *port)
	conn, err := net.ListenUDP("udp", &net.UDPAddr{Port: *port})
	must(err)
	defer conn.Close()

	for {
		buff := make([]byte, 2000)
		n, addr, err := conn.ReadFromUDP(buff)
		must(err)
		fmt.Printf("received %d bytes from %s\n", n, addr)
		fmt.Printf("data: %q\n", string(buff[:n]))

		n, err = conn.WriteToUDP(buff[:n], addr)
		must(err)
		fmt.Printf("sent %d bytes to %s\n", n, addr)
	}
}
