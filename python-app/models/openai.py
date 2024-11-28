import httpx
from enum import Enum
from openai import OpenAI
from dev import Model
from typing import Any, Optional, Union
from pydantic import BaseModel



class DeltaContent(BaseModel):
    """Класс для описания частичных данных в режиме stream"""
    content: Optional[str] = None


class Choice(BaseModel):
    """Класс для описания варианта ответа от модели"""
    index: int
    message: Optional[dict] = None
    delta: Optional[DeltaContent] = None
    finish_reason: Optional[str] = None


class Response(BaseModel):
    """Класс для типизации ответа OpenAI"""
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
    usage: Optional[dict] = None


class OpenAIModels(Enum):
    GPT4o = "gpt-4o"
    GPT4o_1120 = "gpt-4o-2024-11-20"


class OpenAIClient(OpenAI):
    """
    Класс-обертка для OpenAI SDK с возможностью конфигурации клиента и отправки сообщений.
    """
    def __init__(self, api_key: str, api_base: str | None = None, timeout: Union[float, httpx.Timeout] | None = None):
        """
        Инициализация клиента OpenAI.

        :param api_key: Ваш API-ключ для доступа к OpenAI.
        :param api_base: Базовый URL для API (опционально).
        :param timeout: Таймаут запроса (может быть в секундах или объектом Timeout).
        """
        self.api_key = api_key
        self.api_base = api_base or "https://api.openai.com/v1"
        self.timeout = timeout or self._default_timeout()
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base, timeout=self.timeout)

    @staticmethod
    def _default_timeout() -> httpx.Timeout:
        """
        Устанавливает стандартные таймауты для запросов.

        :return Timeout: Объект Timeout с предустановленными значениями.
        """
        return httpx.Timeout(60.0, read=5.0, write=10.0, connect=3.0)


class OpenAIModel(Model):
    def __init__(self, client: OpenAIClient, model: OpenAIModels):
        super().__init__()
        self.client = client
        self.model = model.value

    def __call__(self, messages: list[dict[str, str]], stream: bool = False) -> str:
        """
        Использует OpenAI API для выполнения запроса.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream
        )
        if stream:
            result = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    result += chunk.choices[0].delta.content
                    print(chunk.choices[0].delta.content, end="")
            return result
        else:
            return response.choices[0].message["content"]

    def request(self, prompt: str, **kwargs: Any) -> str:
        """
        Обертка для упрощенного вызова модели через строку prompt.
        """
        messages = [{"role": "user", "content": prompt}]
        return self.__call__(messages=messages, **kwargs)


if __name__ == "__main__":
    api_key = "your_openai_api_key"
    client = OpenAIClient(api_key=api_key)

    model = OpenAIModel(client=client, model=OpenAIModels.GPT4o)

    prompt = "Say this is a test"
    response = model.request(prompt)
    print("\nResponse:", response)
