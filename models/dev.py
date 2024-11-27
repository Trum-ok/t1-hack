from enum import Enum
from pydantic import BaseModel
from typing import Any, Optional
from abc import ABC, abstractmethod


class Models(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LLAMA = "llama"
    GOOGLE = "google"


class Model(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def request(self):
        pass


class TextBlock(BaseModel):
    text: str
    type: str


class Usage(BaseModel):
    input_tokens: int
    output_tokens: int


class Message(BaseModel):
    id: str
    content: list[TextBlock]
    model: str
    role: str
    stop_reason: str
    stop_sequence: Optional[str]
    type: str
    usage: Usage
