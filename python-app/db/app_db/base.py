import asyncpg

from abc import ABC, abstractmethod
from typing import Optional


class Table(ABC):
    """
    Абстрактный класс для таблиц в базе данных.
    Определяет общие методы: create, insert, update, delete, get.
    """
    def __init__(self, pool: asyncpg.Pool):
        """
        Инициализация с подключением к пулу базы данных.

        :param pool: Экземпляр asyncpg.Pool для работы с базой данных.
        """
        self.pool = pool

    @abstractmethod
    async def create(self) -> None:
        """
        Создание структуры таблицы в базе данных.
        """
        pass

    @abstractmethod
    async def insert(self, data: dict) -> int:
        """
        Вставка данных в таблицу.

        :param data: Словарь с данными для вставки.
        :return: Идентификатор вставленной записи.
        """
        pass

    @abstractmethod
    async def update(self, record_id: int, data: dict) -> None:
        """
        Обновление записи в таблице.

        :param record_id: Идентификатор записи.
        :param data: Словарь с данными для обновления.
        """
        pass

    @abstractmethod
    async def delete(self, record_id: int) -> None:
        """
        Удаление записи из таблицы.

        :param record_id: Идентификатор записи.
        """
        pass

    @abstractmethod
    async def get(self, record_id: int) -> Optional[dict]:
        """
        Получение записи из таблицы.

        :param record_id: Идентификатор записи.
        :return: Словарь с данными записи или None.
        """
        pass
