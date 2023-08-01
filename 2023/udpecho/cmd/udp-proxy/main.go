// Simple UDP proxy server.
// Supports only one client at a time.
package main

import (
	"encoding/hex"
	"flag"
	"fmt"
	"net"
	"sync"
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

type proxy struct {
	clientAddr *net.UDPAddr
	serverConn *net.UDPConn
}

var (
	mProxy sync.Mutex
)

func (p *proxy) run(toClient *net.UDPConn) {
	buff := make([]byte, 2000)
	for {
		n, addr, err := p.serverConn.ReadFromUDP(buff)
		must(err)
		fmt.Printf("s->c: received %d bytes from %s\n", n, addr)
		fmt.Println(hex.Dump(buff[:n]))
		// fmt.Printf("s->c: data: %q\n", string(buff[:n]))

		sent, err := toClient.WriteToUDP(buff[:n], p.clientAddr)
		must(err)
		if sent != n {
			panic("sent != n")
		}
		// fmt.Printf("s->c: sent %d bytes to %s\n", n, p.clientAddr)
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

	proxyMap := make(map[string]*proxy)

	// client -> server
	buff := make([]byte, 2000)
	for {
		n, addr, err := clientConn.ReadFromUDP(buff)
		must(err)
		fmt.Printf("received %d bytes from %s\n", n, addr)
		fmt.Println(hex.Dump(buff[:n]))

		mProxy.Lock()
		px, ok := proxyMap[addr.String()]
		if !ok {
			px = &proxy{
				clientAddr: addr,
				serverConn: nil,
			}
			proxyMap[addr.String()] = px
		}
		mProxy.Unlock()

		if px.serverConn == nil {
			c, err := net.Dial("udp", *target)
			must(err)
			// defer c.Close()
			fmt.Printf("connected to %s from %s\n", c.RemoteAddr(), c.LocalAddr())
			px.serverConn = c.(*net.UDPConn)

			go px.run(clientConn)
		}

		sent, err := px.serverConn.Write(buff[:n])
		must(err)
		// fmt.Printf("sent %d bytes (%s => %s)\n", n, px.serverConn.LocalAddr(), px.serverConn.RemoteAddr())
		if sent != n {
			panic("sent != n")
		}
	}
}
