package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"log"
)

type Store struct {
	User string
	Pass string
	DB   string
}

func main() {

	store := Store{"root", "", "ops"}

	con, err := sql.Open(
		"mysql", store.User+":"+store.Pass+"@/"+store.DB)

	log.Printf("%T, %+v", con, con)

	defer con.Close()

	con.SetMaxIdleConns(100)

	if err != nil {
		log.Println(err)
	}

	jobs := make(chan int, 100)
	result := make(chan int, 100)

	query := func(jobs <-chan int) {
		for j := range jobs {
			rows, _ := con.Query("SELECT id, name FROM hosts")
			fmt.Println(rows)

			var id int
			var name string
			for rows.Next() {
				err := rows.Scan(&id, &name)
				if err != nil {
					log.Println(err)
				}
				// fmt.Println(id, name)
			}
			result <- j
		}
	}

	/*
		write := func(jobs <-chan int) {

			for j := range jobs {
				tx, err := con.Begin()

				if err != nil {
					log.Println(err)
				}

				stmt, err := tx.Prepare(
					"INSERT INTO tracker(name, " +
						"value) VALUES (?, ?)")

				if err != nil {
					log.Println(err)
				}

				res, err := stmt.Exec("name", "test")

				if err != nil {
					fmt.Printf("%T, %+v\n", err, err)
					log.Println(err)
					tx.Rollback()
					return
				}

				lastId, err := res.LastInsertId()
				if err != nil {
					log.Println(err)
					tx.Rollback()
					return
				}

				rowCnt, err := res.RowsAffected()
				if err != nil {
					log.Println(err)
					tx.Rollback()
					return
				}

				tx.Rollback()

				fmt.Printf("ID = %d, affected %d\n", lastId, rowCnt)

				result <- j
			}
		}
	*/

	fetchResult := func(results <-chan int) {
		for j := range results {
			fmt.Println("done", j)
		}
	}

	for x := 0; x < 3; x++ {
		go query(jobs)
	}
	for x := 0; x < 10; x++ {
		go fetchResult(result)
	}

	appendJob := func(x int) {
		jobs <- x
	}

	cnt := 0
	for {
		cnt++
		appendJob(cnt)
	}
}
