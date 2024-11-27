# Используем образ Golang для сборки приложения
FROM golang:latest AS builder

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копируем файлы go.mod и go.sum для загрузки зависимостей
COPY go.mod .
COPY go.sum .

# Загрузка зависимостей с помощью go mod download
RUN go mod download

# Копируем исходный код проекта в контейнер
COPY . .

# Переходим в папку internal
WORKDIR /app/app

# Запускаем main.go
CMD ["go", "run", "main.go"]