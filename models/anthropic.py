import httpx
from enum import Enum
from anthropic import AsyncAnthropic


class AnthropicModel(Enum):
    """
    Enum для хранения доступных моделей Anthropic.
    """
    SONNET3_5 = "claude-3-5-sonnet-latest"
    HAIKU3_5 = "claude-3-5-haiku-latest"


class AnthropicClient:
    """
    Класс-обертка для Anthropic SDK с возможностью конфигурации клиента и отправки сообщений.
    """
    def __init__(self, api_key: str, api_base: str | None = None, timeout: float | httpx.Timeout | None = None):
        """
        Инициализация клиента Anthropic.

        :param api_key: Ваш API-ключ для доступа к OpenAI.
        :param api_base: Базовый URL для API (опционально).
        :param timeout: Таймаут запроса (может быть в секундах или объектом Timeout).
        """
        self.api_key = api_key
        self.api_base = api_base or "https://api.anthropic.com/v1"
        self.timeout = timeout or self._default_timeout()
        self.client = AsyncAnthropic(api_key=self.api_key, base_url=self.api_base, timeout=timeout)

    @staticmethod
    def _default_timeout() -> httpx.Timeout:
        """
        Устанавливает стандартные таймауты для запросов.

        :return Timeout: Объект Timeout с предустановленными значениями.
        """
        return httpx.Timeout(60.0, read=5.0, write=10.0, connect=3.0)

    async def count_tokens(self, model: AnthropicModel, user_message: str) -> dict:
        """
        Подсчитывает количество токенов для заданного сообщения.

        :param model: Модель для взаимодействия.
        :param user_message: Сообщение пользователя.
        :return: Словарь с количеством входящих и исходящих токенов.
        """
        try:
            count = await self.client.beta.messages.count_tokens(
                model=model.value,
                messages=[
                    {"role": "user", "content": user_message}
                ],
            )
            return {"input_tokens": count.input_tokens, "output_tokens": count.output_tokens}
        except Exception as e:
            raise RuntimeError(f"Ошибка при подсчёте токенов: {e}") from e


    async def send_message(self, model: AnthropicModel, user_message: str, max_tokens: int = 1024, count_tokens: bool = True) -> dict:
        """
        Асинхронно отправляет сообщение к API Anthropic и возвращает ответ.

        :param model: Модель для взаимодействия.
        :param user_message: Сообщение пользователя.
        :param max_tokens: Максимальное количество токенов.
        :param count_tokens: Флаг для подсчёта токенов перед отправкой сообщения.
        :return: Ответ от API Anthropic.
        """
        token_info = None
        if count_tokens:
            token_info = await self.count_tokens(model, user_message)
            print(f"Подсчитанные токены: {token_info}")

        try:
            response = await self.client.messages.create(
                model=model.value,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
            )
            return {
                "response": response,
                "tokens": token_info,
            }
        except Exception as e:
            raise RuntimeError(f"Ошибка при запросе к Anthropic: {e}") from e


if __name__ == "__main__":
    API_KEY = "api_key"

    anthropic_client = AnthropicClient(api_key=API_KEY)

    model = AnthropicModel.SONNET3_5
    user_message = "Hello, Claude"

    try:
        response = anthropic_client.send_message(model=model, user_message=user_message)
        print("Response:", response)
    except Exception as e:
        print(f"An error occurred: {e}")
