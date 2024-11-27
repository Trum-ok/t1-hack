package main

import (
	"log"

	"github.com/Danila331/HACH-T1/app/servers"
	"github.com/Danila331/HACH-T1/app/store"
)

func main() {
	conn, err := store.ConnectDB()
	if err != nil {
		panic(err)
	}
	defer conn.Close()
	_, err = conn.Exec(`CREATE TABLE IF NOT EXISTS databases (id SERIAL PRIMARY KEY,type TEXT,host TEXT,port TEXT,username TEXT,password TEXT,database_name TEXT)`)
	if err != nil {
		log.Printf("Error: %s", err)
	}
	_, err = conn.Exec("CREATE TABLE IF NOT EXISTS files (id SERIAL PRIMARY KEY, name TEXT, path TEXT)")
	if err != nil {
		log.Printf("Error: %s", err)
	}
	_, err = conn.Exec("CREATE TABLE IF NOT EXISTS websites (id SERIAL PRIMARY KEY, name TEXT, url TEXT)")
	if err != nil {
		log.Printf("Error: %s", err)
	}
	_, err = conn.Exec(`
    CREATE TABLE IF NOT EXISTS nodes (
        id SERIAL PRIMARY KEY,
        node_type TEXT NOT NULL,
        text TEXT NOT NULL,
        should_to_do TEXT
    )
	`)
	if err != nil {
		log.Printf("Error: %s", err)
	}
	err = servers.StartServer()
	if err != nil {
		log.Printf("Error: %s", err)
	}
}
