from typing import Any
from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def request(self):
        pass

