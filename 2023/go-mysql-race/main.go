// https://github.com/go-sql-driver/mysql/issues/1423
// Using sql.RawBytes is dangerous.

package main

import (
	"database/sql"
	"fmt"
	"reflect"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

func must(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	db, err := sql.Open("mysql", "root@tcp(127.0.0.1:3306)/test")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	for i := 0; i < 100; i++ {
		s := fmt.Sprintf("Hello, %v ", i)

		rows, err := db.Query("SELECT repeat(?, 5)", s)
		must(err)
		cols, err := rows.ColumnTypes()
		must(err)

		for rows.Next() {
			val := reflect.New(cols[0].ScanType())
			// fmt.Printf("Value is %+v\n", val)

			err = rows.Scan(val.Interface())
			must(err)
			b := val.Elem().Bytes()
			// fmt.Println(string(b))
			s1 := string(b)

			go func(s1 string, b []byte) {
				for i := 0; i < 1000; i++ {
					time.Sleep(time.Millisecond)
					s2 := string(b)
					if s1 != s2 {
						fmt.Printf("s1: %q, s2: %q\n", s1, s2)
						break
					}
				}
			}(s1, b)
		}
		rows.Close()
	}
}
