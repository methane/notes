package main

import (
	"database/sql"
	"fmt"
	"time"

	_ "go-conncheck/mysql"
)

func main() {
	db, err := sql.Open("mysql", "root:test@tcp(127.0.0.1:3306)/")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	if _, err := db.Exec("SET wait_timeout = 2"); err != nil {
		panic(err)
	}

	sleeping := time.Millisecond * 300
	for {
		var v int
		fmt.Printf("running query... ")
		before := time.Now()
		err := db.QueryRow("SELECT 42").Scan(&v)
		fmt.Printf("took %v\n", time.Since(before))
		if err != nil {
			panic(err)
		}

		fmt.Printf("Sleeping %v...\n", sleeping)
		time.Sleep(sleeping)
		sleeping += time.Millisecond * 300
	}
}
