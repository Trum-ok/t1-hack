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
    def __init__(self, type_: str, parent=None, childs=None, *args, **kwargs):
        self.type_ = type_  # Установка типа ноды
        self.parent = parent  # Родительская нода
        self.childs = childs if childs is not None else []  # Список дочерних нод
        self.input_data = {
            "eoc": False
        }
        self.output_data = {}

    @abstractmethod
    def process(self, input_data: dict) -> dict:
        """
        Обрабатывает входные данные и возвращает результат.
        """
        pass


class GreatingNode(Node):
    def __init__(self, type_: str, parent: Node = None, childs: list[Node] = None, message: str = ""):
        super().__init__(type_, parent, childs)
        self.message = message

    def process(self, input_data: dict) -> dict:
        """
        Возвращает сообщение, добавленное к данным.
        """
        output = input_data.copy()
        output['message'] = self.message
        return output


class MessageNode(Node):
    def __init__(self, type_: str, parent: Node = None, childs: list[Node] = None, message: str = ""):
        super().__init__(type_, parent, childs)
        self.message = message

    def process(self, input_data: dict) -> dict:
        return super().process(input_data)


class TriggerNode(Node):
    def __init__():
        pass


class EoCNode(Node):
    def __init__(self, type_: str, parent=None, childs=None, *args, **kwargs):
        super().__init__(type_, parent, childs, *args, **kwargs)
        self.message = kwargs.get("message", "Conversation ended.")  # Сообщение для конца разговора

    def process(self, input_data: dict) -> dict:
        """
        Возвращает входные данные с добавлением сообщения о завершении разговора.
        """
        output = input_data.copy()
        output['eoc'] = True  # Флаг окончания
        output['message'] = self.message
        return output
