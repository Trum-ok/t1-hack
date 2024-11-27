package store

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
	_ "github.com/lib/pq"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// Новые параметры подключения к базе данных PostgreSQL
// POSTGRESQL_HOST=45.10.43.153
// POSTGRESQL_PORT=5432
// POSTGRESQL_USER=gen_user
// POSTGRESQL_PASSWORD=g!AVY93W<$}d&x
// POSTGRESQL_DBNAME=default_db

// Константы подключения к базе данных PostgreSQL
const (
	POSTGRESQL_HOST     = "45.10.43.153"
	POSTGRESQL_PORT     = 5432
	POSTGRESQL_USER     = "gen_user"
	POSTGRESQL_PASSWORD = "g!AVY93W<$}d&x"
	POSTGRESQL_DBNAME   = "default_db"
)

func ConnectDB() (*sql.DB, error) {
	// Формирование строки подключения
	connStr := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		POSTGRESQL_HOST, POSTGRESQL_PORT, POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_DBNAME,
	)

	// Открытие соединения с базой данных
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("не удалось открыть соединение с PostgreSQL: %v", err)
	}

	// Проверка соединения
	if err = db.Ping(); err != nil {
		return nil, fmt.Errorf("не удалось подключиться к PostgreSQL: %v", err)
	}

	fmt.Println("Успешное подключение к PostgreSQL")
	return db, nil
}

func ConnectToPostgresSql(host, port, user, password, dbname string) (*sql.DB, error) {
	// Строка подключения к базе данных PostgreSQL
	connectionString := fmt.Sprintf("postgres://%s:%s@%s:%s/%s", user, password, host, port, dbname)

	db, err := sql.Open("postgres", connectionString)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %v", err)
	}

	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("failed to ping database: %v", err)
	}

	return db, nil
}

func ConnectToMongoDB(host, port, user, password, dbname string) (*mongo.Client, error) {
	// Формирование строки подключения к базе данных MongoDB с учетом входных параметров
	connectionString := fmt.Sprintf("mongodb://%s:%s@%s:%s/%s", user, password, host, port, dbname)

	clientOptions := options.Client().ApplyURI(connectionString)

	// Подключение к MongoDB
	client, err := mongo.NewClient(clientOptions)
	if err != nil {
		return nil, fmt.Errorf("failed to create MongoDB client: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	err = client.Connect(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to MongoDB: %v", err)
	}

	// Проверка подключения
	err = client.Ping(ctx, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to ping MongoDB: %v", err)
	}

	return client, nil
}

func ConnectToMySQL(host, port, user, password, dbname string) (*sql.DB, error) {
	// Формирование строки подключения к базе данных MySQL с учетом входных параметров
	connectionString := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", user, password, host, port, dbname)

	db, err := sql.Open("mysql", connectionString)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to MySQL database: %v", err)
	}

	// Установка таймаута подключения
	db.SetConnMaxLifetime(time.Minute * 3)
	db.SetMaxOpenConns(10)
	db.SetMaxIdleConns(10)

	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("failed to ping MySQL database: %v", err)
	}

	return db, nil
}

func ConnectToElasticsearch(host, port, user, password string) (*elasticsearch.Client, error) {
	// Формирование строки подключения к базе данных Elasticsearch с учетом входных параметров
	address := fmt.Sprintf("http://%s:%s", host, port)

	cfg := elasticsearch.Config{
		Addresses: []string{address},
		Username:  user,
		Password:  password,
	}

	// Подключение к Elasticsearch
	client, err := elasticsearch.NewClient(cfg)
	if err != nil {
		return nil, fmt.Errorf("failed to create Elasticsearch client: %v", err)
	}

	// Проверка подключения
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	res, err := client.Ping(client.Ping.WithContext(ctx))
	if err != nil {
		return nil, fmt.Errorf("failed to ping Elasticsearch: %v", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		return nil, fmt.Errorf("error response from Elasticsearch: %s", res.String())
	}

	return client, nil
}
