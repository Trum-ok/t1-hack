package models

import "github.com/Danila331/HACH-T1/app/store"

type Website struct {
	ID   int
	Name string
	URL  string
}

type WebsiteInterface interface {
	Create() error
	ReadAll() ([]Website, error)
	Update() error
	Delete() error
}

func (w *Website) Create() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("INSERT INTO websites (name, url) VALUES ($1, $2)", w.Name, w.URL)
	if err != nil {
		return err
	}
	return nil
}

func (w *Website) ReadAll() ([]Website, error) {
	conn, err := store.ConnectDB()
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	rows, err := conn.Query("SELECT * FROM websites")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var websites []Website
	for rows.Next() {
		var website Website
		err := rows.Scan(&website.ID, &website.Name, &website.URL)
		if err != nil {
			return nil, err
		}
		websites = append(websites, website)
	}
	return websites, nil
}

func (w *Website) Update() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("UPDATE websites SET name=$1, url=$2 WHERE id=$3", w.Name, w.URL, w.ID)
	if err != nil {
		return err
	}
	return nil
}

func (w *Website) Delete() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("DELETE FROM websites WHERE id=$1", w.ID)
	if err != nil {
		return err
	}
	return nil
}
