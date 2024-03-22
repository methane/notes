package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

const (
	url = "http://127.0.0.1:8000"
)

func worker(ch chan<- string) {
	for i := 0; i < 10; i++ {
		resp, _ := http.Get(url)
		body, _ := ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		ch <- string(body)
	}
}

func main() {
	ch := make(chan string)

	for i := 0; i < 10; i++ {
		go worker(ch)
	}
	for i := 0; i < 10*10; i++ {
		fmt.Println(<-ch)
	}
}
