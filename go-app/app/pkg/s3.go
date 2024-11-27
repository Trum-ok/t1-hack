package pkg

import (
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

func S3LoadFile(fileName, filePath string) error {
	cfg := aws.Config{
		Credentials: credentials.NewStaticCredentials(
			"TFZV4KUNPJG18KJINWMR",                     // ACCESS_KEY из вашего окружения
			"nJxrnROvFeBOCrm4FADDawCl6OJ7Xn0dQBLkYMan", // SECRET_ACCESS_KEY из вашего окружения
			""), // token необязательный; оставьте пустым, если не нужен
		Endpoint:         aws.String("https://s3.timeweb.cloud"), // ENDPOINT из вашего окружения
		Region:           aws.String("ru-1"),                     // REGION_NAME из вашего окружения
		S3ForcePathStyle: aws.Bool(true),
	}

	// Создание новой сессии S3
	sess := session.Must(session.NewSession(&cfg))

	// Создание нового S3 клиента
	svc := s3.New(sess)

	// Открытие файла
	file, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("unable to open file: %v", err)
	}
	defer file.Close()

	// Создание объекта PutObjectInput
	input := &s3.PutObjectInput{
		Body:   file,
		Bucket: aws.String("9ba75d8d-cb603f95-2e74-49c2-9f16-f8359d6dd8d0"),
		Key:    aws.String(fileName),
	}

	// Загрузка файла в S3
	_, err = svc.PutObject(input)
	if err != nil {
		return fmt.Errorf("error uploading file to S3: %v", err)
	}

	fmt.Printf("File %s uploaded successfully to bucket %s\n", file.Name(), "001b3177-49d13eec-a629-4743-ba8e-e47b1894d535")
	return nil
}
