package servers

import (
	"github.com/Danila331/HACH-T1/app/handlers"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func StartServer() error {
	app := echo.New()

	app.Static("/static", "./static")
	app.Use(middleware.Logger())
	app.Use(middleware.Recover())

	// Group for uploads
	uploads := app.Group("/uploads")
	uploads.GET("/", handlers.UploadsPage)
	uploads.GET("/add", handlers.UploadsAddPage)
	// Group for files
	file := uploads.Group("/add/file")
	file.GET("/", handlers.AddFilePage)
	file.POST("/submit", handlers.AddFileSubmit)
	// Group for database
	database := uploads.Group("/add/database")
	database.GET("/", handlers.AddDatabasePage)
	// Group for postgressql
	postgressql := database.Group("/postgressql")
	postgressql.GET("/", handlers.AddPostgressqlPage)
	postgressql.POST("/submit", handlers.AddPostgressqlSubmit)
	// Group for mysql
	mysql := database.Group("/mysql")
	mysql.GET("/", handlers.AddMysqlPage)
	mysql.POST("/submit", handlers.AddMysqlSubmit)
	// Group for elasticsearch
	elasticsearch := database.Group("/elasticsearch")
	elasticsearch.GET("/", handlers.AddElasticsearchPage)
	elasticsearch.POST("/submit", handlers.AddElasticsearchSubmit)
	// Group for mongodb
	mongodb := database.Group("/mongodb")
	mongodb.GET("/", handlers.AddMongodbPage)
	mongodb.POST("/submit", handlers.AddMongodbSubmit)
	// Group for website
	website := uploads.Group("/add/website")
	website.GET("/", handlers.AddWebsitePage)
	website.POST("/submit", handlers.AddWebsiteSubmit)

	return app.Start(":8081")
}
