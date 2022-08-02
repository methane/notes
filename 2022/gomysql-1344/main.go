package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"math/rand"
	"runtime"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var (
	db *sql.DB
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	var err error
	db, err = sql.Open("mysql", "root:Asd123dsa@tcp(127.0.0.1:3306)/nahry?interpolateParams=true")
	must(err)
	_, err = db.Exec("select 1")
	must(err)

	for i := 0; i < 10; i++ {
		t0 := time.Now()
		insertpatient()
		t1 := time.Now()
		bookapointments()
		t2 := time.Now()
		getpending()
		t3 := time.Now()
		getdone()
		t4 := time.Now()
		getdata()
		t5 := time.Now()
		gettop()
		t6 := time.Now()
		getdatab()
		t7 := time.Now()
		getfulldate()
		t8 := time.Now()
		elapsed := t8.Sub(t0)
		fmt.Printf("%d %v\n", i, elapsed)
		fmt.Printf(" %v %v %v %v %v %v %v %v\n",
			t1.Sub(t0),
			t2.Sub(t1),
			t3.Sub(t2),
			t4.Sub(t3),
			t5.Sub(t4),
			t6.Sub(t5),
			t7.Sub(t6),
			t8.Sub(t7))

		time.Sleep(2 * time.Second)
	}
}

func getfulldate() string {
	//user := c.Locals("user").(*jwt.Token)
	//claims := user.Claims.(jwt.MapClaims)
	////	name := claims["firstname"].(string)
	//
	//cID := claims["cID"].(float64)
	pid := 6769

	result, err := db.Prepare("select concat(p.firstName, ' ', p.middle, ' ', p.lastName, ' ', p.forthName) as fullname,gender,bID,married,barcode,comment,address,if(p2.phone is null, 0, p2.phone)  as phone,rName,occupation,weight,height,cast(Birthdate as date) as Birthdate from profile p left join (select phID, pID, phone from phonefix group by pID) p2 on p.pID = p2.pID left join (select pID, weight, height from bmifix group by pID) B on p.pID = B.pID, religion r where r.rgID = p.rgID and p.pID = ? ")
	defer result.Close()
	if err != nil {
		fmt.Println("error")
	}

	rows, err := result.Query(pid)
	defer rows.Close()
	if err != nil {
		fmt.Println("error")

	}
	columns, err := rows.Columns()
	if err != nil {
		return "0"
	}
	count := len(columns)
	tableData := make([]map[string]interface{}, 0)
	values := make([]interface{}, count)
	valuePtrs := make([]interface{}, count)
	for rows.Next() {
		for i := 0; i < count; i++ {
			valuePtrs[i] = &values[i]
		}
		rows.Scan(valuePtrs...)
		entry := make(map[string]interface{})
		for i, col := range columns {
			var v interface{}
			val := values[i]
			b, ok := val.([]byte)
			if ok {
				v = string(b)
			} else {
				v = val
			}
			entry[col] = v
		}
		tableData = append(tableData, entry)
	}

	currentTime := time.Now().Format("2006-01-02")
	result, err = db.Prepare("select viID,state as done,dob from visitfix where  patientID = ?")
	defer result.Close()
	if err != nil {
		fmt.Println("error")

	}

	rows, err = result.Query(pid)
	defer rows.Close()
	if err != nil {
		fmt.Println("error")

	}
	columns = []string{"viID", "done", "dob"}

	count = len(columns)
	tableDatas := make([]map[string]interface{}, 0)
	values = make([]interface{}, count)
	valuePtrs = make([]interface{}, count)
	for rows.Next() {
		for i := 0; i < count; i++ {

			valuePtrs[i] = &values[i]
		}

		rows.Scan(valuePtrs...)

		entry := make(map[string]interface{})

		for i, col := range columns {
			var v interface{}
			val := values[i]

			b, ok := val.([]byte)

			if ok {
				v = string(b)
			} else {
				v = val
			}
			if i == 2 {
				var state string
				format := "2006-1-2"

				datea, err := time.Parse(format, string(b))
				if err != nil {
					return "0"
				}
				mydate := datea.Format("2006-01-02")
				if mydate == currentTime {
					state = "today"
				}
				if mydate < currentTime {
					state = "older"
				}
				if mydate > currentTime {
					state = "newer"
				}

				entry["state"] = state

			}

			entry[col] = v
		}

		tableDatas = append(tableDatas, entry)
	}
	alldata := [][]map[string]interface{}{tableData, tableDatas}
	_, err = json.Marshal(alldata)
	if err != nil {
		return "0"
	}

	//	fmt.Println(dat)
	return "0"
}
func barcodegen() int {
	for true {
		rand.Seed(time.Now().UnixNano())
		min := 100000
		max := 999999
		myradn := rand.Intn(max-min+1) + min

		result, err := db.Prepare("select 1 from profile where barcode = ?")
		if err != nil {
			break

		}
		defer result.Close()

		inse, err := result.Exec(myradn) // I

		must(err)
		count, err := inse.RowsAffected()

		if count == 0 {
			return myradn
		}
	}
	return 0
}
func getpending() string {

	datea := time.Now().Format("2006-01-02")

	result, err := db.Prepare("select fullname, barcode, CAST(pay AS VARCHAR(10)) as daybill, data, viID,pID,allvisit,if(paid is null,0,paid) as paid from patientvisit2 where state = 0 and forWhen = date(?) and cID = ?  ")
	if err != nil {
		return "0"

	}
	defer result.Close()
	rows, err := result.Query(datea, 8)
	defer rows.Close()

	if err != nil {
		return "0"

	}
	columns, err := rows.Columns()
	if err != nil {
		return "err"
	}
	count := len(columns)
	tableData := make([]map[string]interface{}, 0)
	values := make([]interface{}, count)
	valuePtrs := make([]interface{}, count)
	for rows.Next() {
		for i := 0; i < count; i++ {
			valuePtrs[i] = &values[i]
		}
		rows.Scan(valuePtrs...)
		entry := make(map[string]interface{})
		for i, col := range columns {
			var v interface{}
			val := values[i]
			b, ok := val.([]byte)
			if ok {
				v = string(b)
			} else {
				v = val
			}
			entry[col] = v
		}
		tableData = append(tableData, entry)
	}
	jsonData, err := json.Marshal(tableData)
	//fmt.Println(jsonData)
	_ = jsonData
	if err != nil {
		return "err"
	}

	return "c.SendString(string(jsonData))"
}

func getdone() string {
	datea := time.Now().Format("2006-01-02")
	cID := 8

	result, err := db.Prepare("select fullname, barcode, CAST(pay AS VARCHAR(10)) as daybill, data, viID,pID,allvisit,if(paid is null,0,paid) as paid from patientvisit2 where state = 1 and forWhen = date(?) and cID = ?  ")
	if err != nil {
		return "0"

	}
	defer result.Close()
	rows, err := result.Query(datea, cID)
	defer rows.Close()
	if err != nil {
		return "0"

	}
	columns, err := rows.Columns()
	if err != nil {
		return "err"
	}
	count := len(columns)
	tableData := make([]map[string]interface{}, 0)
	values := make([]interface{}, count)
	valuePtrs := make([]interface{}, count)
	for rows.Next() {
		for i := 0; i < count; i++ {
			valuePtrs[i] = &values[i]
		}
		rows.Scan(valuePtrs...)
		entry := make(map[string]interface{})
		for i, col := range columns {
			var v interface{}
			val := values[i]
			b, ok := val.([]byte)
			if ok {
				v = string(b)
			} else {
				v = val
			}
			entry[col] = v
		}
		tableData = append(tableData, entry)
	}
	jsonData, err := json.Marshal(tableData)
	if err != nil {
		return "err"
	}
	//fmt.Println(jsonData)
	_ = jsonData

	return "c.SendString(string(jsonData))"
}

func getdata() string {

	var t0, t1 time.Time
	t0 = time.Now()
	cID := 8

	timing := func() {
		t1 = time.Now()
		_, _, line, _ := runtime.Caller(1)
		fmt.Println(line, t1.Sub(t0))
		t0 = t1
	}

	currentTime := time.Now().Format("2006-01-02")

	var tpen int
	err := db.QueryRow("select count(1) as temp from patientvisit where state = 0 and forWhen = date(?) and cID = ?   ", currentTime, cID).Scan(&tpen)
	must(err)

	timing()

	var tcomp int
	err = db.QueryRow("select count(1) as temp from patientvisit where state = 1 and forWhen = date(?) and cID = ?   ", currentTime, cID).Scan(&tcomp)
	must(err)
	timing()

	var compa int
	err = db.QueryRow("select count(1) as temp from patientvisit where state = 1 and  cID = ? ", cID).Scan(&compa)
	must(err)
	timing()

	var allapp int
	err = db.QueryRow("select count(1) as temp from patientvisit where   cID = ?", cID).Scan(&allapp)
	must(err)
	timing()

	var allpa int
	err = db.QueryRow("select count(1) as temp from profile where aID = 4 and   cID = ? ", cID).Scan(&allpa)
	must(err)
	timing()

	return "c.JSON()"
}

func gettop() string {

	cID := 8
	datea := time.Now().Format("2006-01-02")
	result, err := db.Prepare("select fullname, viID from patientvisit2 where state = 0 and forWhen = date(?) and cID = ? limit 2 ")
	defer result.Close()
	if err != nil {
		return "0"

	}

	rows, err := result.Query(datea, cID)
	defer rows.Close()
	if err != nil {
		return "0"

	}
	columns, err := rows.Columns()

	if err != nil {
		return "err"
	}
	count := len(columns)
	tableData := make([]map[string]interface{}, 0)
	values := make([]interface{}, count)
	valuePtrs := make([]interface{}, count)
	for rows.Next() {
		for i := 0; i < count; i++ {
			valuePtrs[i] = &values[i]
		}
		rows.Scan(valuePtrs...)
		entry := make(map[string]interface{})
		for i, col := range columns {
			var v interface{}
			val := values[i]
			b, ok := val.([]byte)
			if ok {
				v = string(b)
			} else {
				v = val
			}
			entry[col] = v
		}
		tableData = append(tableData, entry)
	}
	jsonData, err := json.Marshal(tableData)
	if err != nil {
		return "err"
	}
	//fmt.Println(jsonData)
	_ = jsonData

	return "c.SendString(string(jsonData))"

}

func getdatab() string {

	cID := 8

	datea := time.Now().Format("2006-01-02")

	result, err := db.Prepare("select count(1) as me from patientvisit where  forWhen = date(?) and data > 0 and cID = ?  ")
	defer result.Close()
	if err != nil {
		return "0"

	}
	var allextrap int
	err = result.QueryRow(datea, cID).Scan(&allextrap) // WHERE number = 13
	if err != nil {
		allextrap = 0
	}

	result, err = db.Prepare("select sum(data) as alld  from patientvisit where  forWhen = date(?) and cID = ?  ")

	defer result.Close()
	if err != nil {
		return "0"

	}
	var allextram int
	err = result.QueryRow(datea, cID).Scan(&allextram) // WHERE number = 13
	if err != nil {
		allextram = 0
	}

	result, err = db.Prepare("select sum(pay) as alld from patientvisit where  forWhen = date(?) and cID = ? ")
	defer result.Close()
	if err != nil {
		return "0"

	}
	var allbillm int

	err = result.QueryRow(datea, cID).Scan(&allbillm) // WHERE number = 13
	defer result.Close()
	if err != nil {

		allbillm = 0
	}

	result, err = db.Prepare("select count(1) as me from patientvisit where  forWhen = date(?) and pay > 0 and cID = ? ")
	defer result.Close()

	if err != nil {
		return "0"

	}
	var allbillp int
	err = result.QueryRow(datea, cID).Scan(&allbillp) // WHERE number = 13
	if err != nil {
		allbillp = 0
	}

	return ""
}

func insertpatient() string {

	cID := 8
	first := "hhh hh hh "

	phone_no := ""

	religion := ""
	result, err := db.Prepare("select rgID from religion where rName = ?")
	must(err)
	defer result.Close()

	var rgID int64
	err = result.QueryRow(religion, cID).Scan(&rgID) // WHERE number = 13
	if err != nil {
		result, err := db.Prepare("insert into religion ( rName) value (?)")
		defer result.Close()
		if err != nil {
			return "0"

		}

		inse, err := result.Exec(religion) // I

		if err != nil {
			fmt.Println(err.Error())
		}
		rgID, _ = inse.LastInsertId()
	}
	var weightI = "0"

	var heightI = "0"

	barcode := barcodegen()

	result, err = db.Prepare("insert into profile (firstName,cID,aID,barcode) values (?,?,4,?)")
	defer result.Close()
	if err != nil {
		return "0"

	}
	var pID int64

	inse, err := result.Exec(first, cID, barcode) // I
	if err != nil {
		fmt.Println(err.Error())
	}
	pID, _ = inse.LastInsertId()

	result, err = db.Prepare("insert into impression(pID)values (?)")
	defer result.Close()
	if err != nil {
		return "0"

	}

	_, err = result.Exec(pID) // I
	if err != nil {
		fmt.Println(err.Error())
	}
	result, err = db.Prepare("insert into phistory(pID)values (?)")
	defer result.Close()
	if err != nil {
		return "0"

	}

	_, err = result.Exec(pID) // I
	if err != nil {
		fmt.Println(err.Error())
	}
	if phone_no != "" {
		result, err = db.Prepare("insert into phone( pID, phone) value (?,?)")
		defer result.Close()
		if err != nil {
			return "0"

		}

		_, err = result.Exec(pID, phone_no) // I
		if err != nil {
			fmt.Println(err.Error())
		}
	}
	result, err = db.Prepare("insert into BMI( pID, weight,height) value (?,?,?)")
	defer result.Close()
	if err != nil {
		return "0"

	}

	_, err = result.Exec(pID, weightI, heightI) // I
	if err != nil {
		fmt.Println(err.Error())
	}

	return "0"
}
func bookapointments() string {

	cID := 8
	datea := time.Now().Format("2006-01-02")
	pid := 1
	pay := 1500

	result, err := db.Prepare(" select pID from profile where daID  != 1 and aID = 2 and cID = ? limit 1 ")
	defer result.Close()
	if err != nil {
		return ""

	}

	var doc int
	err = result.QueryRow(cID).Scan(&doc) // WHERE number = 13
	if err != nil {

		return "0"

	}
	result, err = db.Prepare(" select 1 from visit where forWhen = ? and patientID = ? and cID = ? and doctorID = ? ")
	defer result.Close()
	if err != nil {
		return "0"

	}

	var docs int
	err = result.QueryRow(datea, pid, cID, doc).Scan(&docs)

	// WHERE number = 13
	if docs == 0 {

		result, err := db.Prepare("insert into visit(patientID, doctorID, cID,forWhen) value (?,?,?,?)")
		defer result.Close()
		if err != nil {
			return "0"

		}

		inse, err := result.Exec(pid, doc, cID, datea) // I
		if err != nil {
			fmt.Println(err.Error())
		}

		viID, err := inse.LastInsertId()
		if err != nil {
			fmt.Println(err.Error())
		}

		result, err = db.Prepare("insert into payment(pay, comment, viID) values (?,'',?)")
		defer result.Close()
		if err != nil {
			return "0"

		}

		_, err = result.Exec(pay, viID) // I
		if err != nil {
			fmt.Println(err.Error())
		}
		result, err = db.Prepare("insert into  vdetail( viID) value (?)")
		defer result.Close()
		if err != nil {
			return "0"

		}

		_, err = result.Exec(viID) // I
		if err != nil {
			fmt.Println(err.Error())
		}
		return "0"

	}

	return "0"
}
