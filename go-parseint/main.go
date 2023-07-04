package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	db, err := sql.Open("mysql", "root@tcp(127.0.0.1)/")
	must(err)

	var v any
	db.QueryRow("SELECT 123 WHERE ? = 1", 1).Scan(&v)
	fmt.Printf("%T %v\n", v, v)

	db.QueryRow("SELECT 123 WHERE 1 = 1").Scan(&v)
	fmt.Printf("%T %v\n", v, v)
}
