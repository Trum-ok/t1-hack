from enum import Enum
from abc import ABC, abstractmethod


class NodeTypes(Enum):
    GREETING = "Приветственная"
    TRIGGER = "Триггер"
    QUESTION = "Вопрос"
    CONDITION = "Условие"
    REDIRECT = "Редирект"
    TRANSFER_TO_MANAGER = "Перевод на менеджера"
    MESSAGE = "Сообщение"


class Node(ABC):
    """
    Класс ноды, от которого наследуются все остальные ноды
    """
    def __init__(self, type_, parent, childs):
        self.type_: NodeTypes = None
        self.parent: Node = None
        self.childs: list[Node] = []

    @abstractmethod
    def process(self, input_data: dict) -> dict:
        """
        Обрабатывает входные данные и возвращает результат.
        """
        pass


class GreatingNode(Node):
    def __init__(self, type_, parent, childs, ):
        super().__init__(type_, parent, childs)


class MessageNode(Node):
    def __init__():
        pass


class TriggerNode(Node):
    def __init__():
        pass
