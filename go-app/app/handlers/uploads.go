package handlers

import (
	"path/filepath"
	"text/template"

	"github.com/Danila331/HACH-T1/app/models"
	"github.com/labstack/echo/v4"
)

type UploadPage struct {
	Files    []models.File
	Dbs      []models.Database
	Websites []models.Website
}

func UploadsPage(c echo.Context) error {
	var file models.File
	var db models.Database
	var website models.Website

	files, err := file.ReadAll()
	if err != nil {
		return err
	}
	dbs, err := db.ReadAll()
	if err != nil {
		return err
	}
	websites, err := website.ReadAll()
	if err != nil {
		return err
	}
	var uploadpage = UploadPage{
		Files:    files,
		Dbs:      dbs,
		Websites: websites,
	}

	htmlFiles := []string{
		filepath.Join("./", "templates", "uploads.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "uploads", uploadpage)
	return nil
}

func UploadsAddPage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "upload_add.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "upload_add", nil)
	return nil
}
