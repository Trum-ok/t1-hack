package pkg

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

// Payload представляет структуру данных, которую вы отправляете.
type Payload struct {
	Data string `json:"data"`
}

// sendRequest отправляет HTTP-запрос на указанный URL с данными в JSON-формате.
func sendRequest(url string, payload Payload) (string, error) {
	// Преобразуем данные в JSON
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return "", fmt.Errorf("ошибка кодирования JSON: %v", err)
	}

	// Создаём новый HTTP-запрос
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return "", fmt.Errorf("ошибка создания HTTP-запроса: %v", err)
	}

	// Устанавливаем заголовки
	req.Header.Set("Content-Type", "application/json")

	// Отправляем запрос с помощью HTTP-клиента
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("ошибка отправки HTTP-запроса: %v", err)
	}
	defer resp.Body.Close()

	// Читаем ответ
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("ошибка чтения ответа: %v", err)
	}

	// Возвращаем тело ответа как строку
	return string(body), nil
}
