package models

import "github.com/Danila331/HACH-T1/app/store"

type Database struct {
	ID           int
	Type         string
	Host         string
	Port         string
	UserName     string
	Password     string
	DatabaseName string
}

type DatabaseInterface interface {
	Create() error
	ReadAll() ([]Database, error)
	Update() error
	Delete() error
}

func (d *Database) Create() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("INSERT INTO databases (type, host, port, username, password, database_name) VALUES ($1, $2, $3, $4, $5, $6)", d.Type, d.Host, d.Port, d.UserName, d.Password, d.DatabaseName)
	if err != nil {
		return err
	}
	return nil
}

func (d *Database) ReadAll() ([]Database, error) {
	conn, err := store.ConnectDB()
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	rows, err := conn.Query("SELECT * FROM databases")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var databases []Database
	for rows.Next() {
		var database Database
		err := rows.Scan(&database.ID, &database.Type, &database.Host, &database.Port, &database.UserName, &database.Password, &database.DatabaseName)
		if err != nil {
			return nil, err
		}
		databases = append(databases, database)
	}
	return databases, nil
}

func (d *Database) Update() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("UPDATE databases SET host=$1, port=$2, username=$3, password=$4, database_name=$5 WHERE id=$6", d.Host, d.Port, d.UserName, d.Password, d.DatabaseName, d.ID)
	if err != nil {
		return err
	}
	return nil
}

func (d *Database) Delete() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("DELETE FROM databases WHERE id=$1", d.ID)
	if err != nil {
		return err
	}
	return nil
}
