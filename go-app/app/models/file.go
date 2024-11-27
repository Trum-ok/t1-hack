package models

import "github.com/Danila331/HACH-T1/app/store"

type File struct {
	ID   int
	Name string
	Path string
}

type FileInterface interface {
	Create() error
	ReadAll() ([]File, error)
	Update() error
	Delete() error
}

func (f *File) Create() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("INSERT INTO files (name, path) VALUES ($1, $2)", f.Name, f.Path)
	if err != nil {
		return err
	}
	return nil
}

func (f *File) ReadAll() ([]File, error) {
	conn, err := store.ConnectDB()
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	rows, err := conn.Query("SELECT * FROM files")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var files []File
	for rows.Next() {
		var file File
		err := rows.Scan(&file.ID, &file.Name, &file.Path)
		if err != nil {
			return nil, err
		}
		files = append(files, file)
	}
	return files, nil
}

func (f *File) Update() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("UPDATE files SET name=$1, path=$2 WHERE id=$3", f.Name, f.Path, f.ID)
	if err != nil {
		return err
	}
	return nil
}

func (f *File) Delete() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("DELETE FROM files WHERE id=$1", f.ID)
	if err != nil {
		return err
	}
	return nil
}
