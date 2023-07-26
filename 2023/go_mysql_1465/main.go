// https://github.com/go-sql-driver/mysql/issues/1465
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
	//connectionString := fmt.Sprintf("%s:%s@tcp(%s)/%s?parseTime=true&interpolateParams=true", "root", "", "127.0.0.1:3306", "")
	connectionString := fmt.Sprintf("%s:%s@tcp(%s)/%s?parseTime=true", "root", "", "127.0.0.1:3306", "")

	db, err := sql.Open("mysql", connectionString)
	if err != nil {
		panic(err)
	}

	_, err = db.Exec("DROP DATABASE IF EXISTS test")
	must(err)
	_, err = db.Exec("CREATE DATABASE test")
	must(err)
	_, err = db.Exec("USE test")
	must(err)
	_, err = db.Exec(testSchema)
	must(err)

	_, err = db.Exec("INSERT INTO test_table (json) VALUES (?)", `{"name": "John", "alive": true}`)
	must(err)

	// query := "SELECT * FROM test_table"
	// rows, err := db.Query(query)

	// query := "SELECT * FROM test_table WHERE json->'$.alive' = CAST(true AS JSON)"
	// rows, err := db.Query(query)

	query := "SELECT * FROM test_table WHERE json->'$.alive' = CAST(? AS JSON)"
	rows, err := db.Query(query, "true") // Not true, but "true"!
	must(err)

	cs, err := rows.Columns()
	must(err)
	fmt.Println(cs)

	for rows.Next() {
		var id int
		var json string
		must(rows.Scan(&id, &json))
		fmt.Println(id, json)
	}
	must(rows.Err())
	must(rows.Close())
}

const testSchema = `
CREATE TABLE IF NOT EXISTS test_table (
	id INT NOT NULL AUTO_INCREMENT,
	json JSON,
	PRIMARY KEY (id)
	) ENGINE=InnoDB;`
