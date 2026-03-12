package main

import (
	"log"
	"net/http"
	"time"
	"math/rand"
)

func rootHandler(w http.ResponseWriter, r *http.Request) {
	time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	w.Write([]byte("Hello, World\n"))
}

func postHandler(w http.ResponseWriter, r *http.Request) {
	time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
	w.WriteHeader(http.StatusCreated)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", rootHandler)
	mux.HandleFunc("/post201", postHandler)

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
