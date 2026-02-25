package main

import (
	"fmt"
	"log"
	"net/http"
)

func rootHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	_, _ = fmt.Fprintf(w, `<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Go HTTP/2 + TLS</title>
</head>
<body>
  <h1>Go HTTP/2 + TLS で動作中</h1>
  <p>Protocol: %s</p>
  <p>Path: %s</p>
</body>
</html>`, r.Proto, r.URL.Path)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", rootHandler)

	addr := ":8443"
	server := &http.Server{
		Addr:    addr,
		Handler: mux,
	}

	log.Printf("Starting HTTPS server on https://localhost%s", addr)
	log.Printf("Using cert: certs/localhost.crt, key: certs/localhost.key")
	if err := server.ListenAndServeTLS("certs/localhost.crt", "certs/localhost.key"); err != nil {
		log.Fatal(err)
	}
}
