// Simple UDP proxy server.
// Supports only one client at a time.
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

// serverToClient reads from serverConn and writes to clientConn.
func serverToClient(conn, clientConn *net.UDPConn, clientAddr *net.UDPAddr) {
	fmt.Printf("s->c: clientConn.remoteaddr = %v\n", clientConn.RemoteAddr())
	fmt.Printf("s->c: clientAddr = %v\n", clientAddr)

	buff := make([]byte, 2000)
	for {
		n, addr, err := conn.ReadFromUDP(buff)
		must(err)
		fmt.Printf("s->c: received %d bytes from %s\n", n, addr)
		fmt.Printf("s->c: data: %q\n", string(buff[:n]))

		n, err = clientConn.WriteToUDP(buff[:n], clientAddr)
		must(err)
		fmt.Printf("  s->c: sent %d bytes to %s\n", n, clientAddr)
	}
}

func main() {
	port := flag.Int("port", 7001, "port to listen")
	target := flag.String("target", "localhost:7000", "target to proxy")
	flag.Parse()

	fmt.Printf("listening on port %d\n", *port)
	clientConn, err := net.ListenUDP("udp", &net.UDPAddr{Port: *port})
	must(err)
	defer clientConn.Close()

	c, err := net.Dial("udp", *target)
	must(err)
	defer c.Close()
	fmt.Printf("connected to %s from %s\n", c.RemoteAddr(), c.LocalAddr())
	serverConn := c.(*net.UDPConn)

	serverStarted := false

	// client -> server
	buff := make([]byte, 2000)
	for {
		n, addr, err := clientConn.ReadFromUDP(buff)
		must(err)
		fmt.Printf("received %d bytes from %s\n", n, addr)

		n2, err := serverConn.Write(buff[:n])
		must(err)
		fmt.Printf("  sent %d bytes to %s\n", n2, serverConn.RemoteAddr())
		if n != n2 {
			panic("bytes mismatch")
		}

		if !serverStarted {
			serverStarted = true
			go serverToClient(serverConn, clientConn, addr)
		}
	}

}
