import httpx
from enum import Enum
from anthropic import AsyncAnthropic


class AnthropicModel(Enum):
    """
    Enum для хранения доступных моделей Anthropic.
    """
    SONNET3_5 = "claude-3-5-sonnet-latest"
    HAIKU3_5 = "claude-3-5-haiku-latest"
    # SONNET3_5 = "claude-3-5-sonnet-20241022"
    # HAIKU3_5 = "claude-3-5-haiku-20241022"


class AnthropicClient:
    """
    Класс-обертка для Anthropic SDK с возможностью конфигурации клиента и отправки сообщений.
    """
    def __init__(self, api_key: str, timeout: float | httpx.Timeout | None = None):
        """
        Инициализация клиента Anthropic.

        :param api_key: Ваш API-ключ для доступа к OpenAI.
        :param api_base: Базовый URL для API (опционально).
        :param timeout: Таймаут запроса (может быть в секундах или объектом Timeout).
        """
        self.api_key = api_key
        self.timeout = timeout or self._default_timeout()
        self.client = AsyncAnthropic(api_key=self.api_key, timeout=timeout)

    @staticmethod
    def _default_timeout() -> httpx.Timeout:
        """
        Устанавливает стандартные таймауты для запросов.

        :return Timeout: Объект Timeout с предустановленными значениями.
        """
        return httpx.Timeout(60.0, read=5.0, write=10.0, connect=3.0)


    async def send_message(self, model: AnthropicModel, user_message: str, max_tokens: int = 1024) -> dict:
        """
        Асинхронно отправляет сообщение к API Anthropic и возвращает ответ.

        :param model: Модель для взаимодействия.
        :param user_message: Сообщение пользователя.
        :param max_tokens: Максимальное количество токенов.

        :return: Ответ от API Anthropic.
        """

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
                "response": response
            }
        except Exception as e:
            raise RuntimeError(f"Ошибка при запросе к Anthropic: {e}") from e


if __name__ == "__main__":
    import os
    import asyncio
    from dotenv import load_dotenv

    load_dotenv(override=True)
    API_KEY = os.getenv("ANTHROPIC_API")

    anthropic_client = AnthropicClient(api_key=API_KEY)

    model = AnthropicModel.HAIKU3_5
    user_message = "Hello, Claude"

    try:
        response = asyncio.run(anthropic_client.send_message(model=model, user_message=user_message, max_tokens=512))
        print("Response:", response)

        """
        Пример ответа
        {'response': Message(id='msg_01LGcgnuHLrYQW8kLbPGi23C',
                             content=[TextBlock(text="Hi! I'm Claude. How can I help you today?", type='text')],
                             model='claude-3-5-sonnet-20241022',
                             role='assistant',
                             stop_reason='end_turn',
                             stop_sequence=None,
                             type='message',
                             usage=Usage(input_tokens=10, output_tokens=16))
        }
        """
    except Exception as e:
        print(e)
