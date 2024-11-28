# ruff: noqa: F401, F841
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import logging
import asyncpg

from flask import Flask
# from elasticsearch import Elasticsearch
# from redis import Redis

from config import Config
from db.app_db.main import Database
from utils.log import formatter  # Логгер настроен в utils.log

flask_logger = logging.getLogger("web")
# TODO: починить логи


class T1App(Flask):
    def __init__(self, import_name, db=None, **kwargs):
        """
        Расширенный класс Flask с поддержкой указания базы данных.

        :param import_name: Имя приложения.
        :param db: Объект базы данных (по умолчанию None).
        :param kwargs: Дополнительные аргументы, передаваемые в Flask.
        """
        super().__init__(import_name, **kwargs)
        self.db: Database = db


async def get_pool() -> asyncpg.Pool:
    """
    Создание пула подключений к базе данных PostgreSQL.
    """
    try:
        pool = await asyncpg.create_pool(
            host=Config.PG_HOST,
            port=Config.PG_PORT,
            user=Config.PG_USER,
            password=Config.PG_PASS,
            database=Config.PG_DATA,
        )
        flask_logger.info("Соединение с базой данных PostgreSQL установлено.")
        return pool
    except Exception as e:
        flask_logger.error(f"Ошибка подключения к БД PostgreSQL: {e}", exc_info=True)
        raise


def create_app(config_class=Config) -> T1App:
    """
    Создает и настраивает Flask приложение.
    """
    app = T1App(__name__)
    app.config.from_object(config_class)

    # Инициализация базы данных
    pool = asyncio.run(get_pool())
    db = Database(pool)
    asyncio.run(db.create())

    app.db = db

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.knowlege_base import bp as knb_bp
    app.register_blueprint(knb_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Логирование запуска приложения
    flask_logger.info("Flask приложение успешно запущено.")
    return app


app_ = create_app()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)
    app_.run(host=os.getenv("HOST", '0.0.0.0'), port=5000, debug=True)
