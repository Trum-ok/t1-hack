package handlers

import (
	"net/http"
	"path/filepath"
	"text/template"

	"github.com/Danila331/HACH-T1/app/models"
	"github.com/labstack/echo/v4"
)

func AddDatabasePage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "databases.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "databases", nil)
	return nil
}

func AddPostgressqlPage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "database", "postgres_add.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "postgres_add", nil)
	return nil
}

// Функция AddPostgressqlSubmit принимает данные из формы и создает новую запись в базе данных
func AddPostgressqlSubmit(c echo.Context) error {
	host := c.FormValue("host")
	port := c.FormValue("port")
	user := c.FormValue("user")
	password := c.FormValue("password")
	dbname := c.FormValue("dbname")
	var db = models.Database{
		Type:         "postgressql",
		Host:         host,
		Port:         port,
		UserName:     user,
		Password:     password,
		DatabaseName: dbname,
	}
	err := db.Create()
	if err != nil {
		return c.String(http.StatusInternalServerError, err.Error())
	}
	return c.String(http.StatusOK, "Postgressql submit")
}

func AddMysqlPage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "database", "mysql_add.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "mysql_add", nil)
	return nil
}

// Функция AddMysqlSubmit принимает данные из формы и создает новую запись в базе данных
func AddMysqlSubmit(c echo.Context) error {
	host := c.FormValue("host")
	port := c.FormValue("port")
	user := c.FormValue("user")
	password := c.FormValue("password")
	dbname := c.FormValue("dbname")
	var db = models.Database{
		Type:         "mysql",
		Host:         host,
		Port:         port,
		UserName:     user,
		Password:     password,
		DatabaseName: dbname,
	}
	err := db.Create()
	if err != nil {
		return c.String(http.StatusInternalServerError, err.Error())
	}
	return c.String(http.StatusOK, "Mysql submit")
}

func AddElasticsearchPage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "database", "elastic_add.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "elastic_add", nil)
	return nil
}

// Функция AddElasticsearchSubmit принимает данные из формы и создает новую запись в базе данных
func AddElasticsearchSubmit(c echo.Context) error {
	host := c.FormValue("host")
	port := c.FormValue("port")
	user := c.FormValue("user")
	password := c.FormValue("password")
	var db = models.Database{
		Type:         "elasticsearch",
		Host:         host,
		Port:         port,
		UserName:     user,
		Password:     password,
		DatabaseName: "",
	}
	err := db.Create()
	if err != nil {
		return c.String(http.StatusInternalServerError, err.Error())
	}
	return c.String(http.StatusOK, "Elasticsearch submit")
}

func AddMongodbPage(c echo.Context) error {
	htmlFiles := []string{
		filepath.Join("./", "templates", "database", "mongodb_add.html"),
	}

	templ, err := template.ParseFiles(htmlFiles...)
	if err != nil {
		return err
	}

	templ.ExecuteTemplate(c.Response(), "mongodb_add", nil)
	return nil
}

// Функция AddMongodbSubmit принимает данные из формы и создает новую запись в базе данных
func AddMongodbSubmit(c echo.Context) error {
	host := c.FormValue("host")
	port := c.FormValue("port")
	user := c.FormValue("user")
	password := c.FormValue("password")
	databasename := c.FormValue("dbname")
	var db = models.Database{
		Type:         "mongodb",
		Host:         host,
		Port:         port,
		UserName:     user,
		Password:     password,
		DatabaseName: databasename,
	}
	err := db.Create()
	if err != nil {
		return c.String(http.StatusInternalServerError, err.Error())
	}
	return c.String(http.StatusOK, "Mongodb submit")
}
