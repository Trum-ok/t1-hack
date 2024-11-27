import asyncpg
import logging
import db.app_db.tables as tables

logger = logging.getLogger("DB")


class Database:
    """
    Класс для работы с базой данных PostgreSQL с использованием asyncpg.
    Управляет пулом соединений и доступом к таблицам.
    """
    def __init__(self, pool: asyncpg.Pool):
        """
        Инициализация класса Database.

        :param pool: Пул соединений с базой данных PostgreSQL.
        """
        self.pool = pool
        self.files = tables.FilesTable(self.pool)
        self.webs = tables.WebsitesTable(self.pool)
        self.dbs = tables.DatabasesTable(self.pool)

    async def create(self) -> None:
        """
        Создание таблиц в БД

        Вызывает метод create() для всех таблиц.
        """
        try:
            await self.files.create()
            await self.webs.create()
            await self.dbs.create()
            logger.info("Таблицы созданы")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц: {e}", exc_info=True)
