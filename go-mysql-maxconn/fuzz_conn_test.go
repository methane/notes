package main

import (
	"database/sql"
	"testing"
	"time"
	"fmt"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

func FuzzConn(f *testing.F){
	db, _ := sql.Open("mysql", "root@tcp(127.0.0.1:3306)/")
	db.SetMaxOpenConns(2)
	db.SetMaxIdleConns(2)
	db.SetConnMaxIdleTime(10 * time.Second)
	db.SetConnMaxLifetime(10 * time.Second)
	fmt.Println("start")

	f.Fuzz(func(t *testing.T, a int) {
		go func() {
			r, _ := db.Query(fmt.Sprintf("select sleep(10) /* %d */", os.Getpid()))
			r.Close()
		}()
	})

	fmt.Println(db.Stats())
}
