from asyncpg import Pool
from typing import Coroutine, Any
from db.app_db.base import Table


class FilesTable(Table):
    def __init__(self, pool: Pool):
        super().__init__(pool)

    def create(self) -> Coroutine[Any, Any, None]:
        return super().create()

    def delete(self, record_id: int) -> Coroutine[Any, Any, None]:
        return super().delete(record_id)

    def insert(self, data: dict) -> Coroutine[Any, Any, int]:
        return super().insert(data)

    def update(self, record_id: int, data: dict) -> Coroutine[Any, Any, None]:
        return super().update(record_id, data)

    def get(self, record_id: int) -> Coroutine[Any, Any, dict | None]:
        return super().get(record_id)
