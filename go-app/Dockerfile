FROM golang:latest AS builder

WORKDIR /app

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .
WORKDIR /app/app

CMD ["go", "run", "main.go"]
