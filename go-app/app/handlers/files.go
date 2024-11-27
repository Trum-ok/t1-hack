package handlers

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"text/template"

	"github.com/Danila331/HACH-T1/app/models"
	"github.com/Danila331/HACH-T1/app/pkg"
	"github.com/labstack/echo/v4"
)

func AddFilePage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "file_add.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "file_add", nil)
	return nil
}

func AddFileSubmit(c echo.Context) error {
	// Получаем файл из формы
	file, err := c.FormFile("file")
	if err != nil {
		return err
	}

	// Открываем файл для чтения
	src, err := file.Open()
	if err != nil {
		return err
	}
	defer src.Close()

	// Создаем путь для сохранения файла на локальной машине
	uploadsDir := "uploads"
	if err := os.MkdirAll(uploadsDir, os.ModePerm); err != nil {
		return err
	}
	dstPath := filepath.Join(uploadsDir, file.Filename)

	// Создаем файл на локальной машине
	dst, err := os.Create(dstPath)
	if err != nil {
		return err
	}
	defer dst.Close()

	// Копируем содержимое файла из запроса в файл на локальной машине
	if _, err = io.Copy(dst, src); err != nil {
		return err
	}

	fmt.Println(dstPath)

	println("File uploaded successfully")
	// Закончился код загрузки файла
	var modelFile = models.File{
		Name: file.Filename,
		Path: string(dstPath),
	}

	err = modelFile.Create()
	if err != nil {
		return err
	}

	err = pkg.S3LoadFile(file.Filename, dstPath)
	if err != nil {
		return err
	}
	return nil
}
