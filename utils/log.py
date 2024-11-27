import os
import logging
from dotenv import load_dotenv

# Загружаем .env файл
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), override=True)

if not os.path.exists(os.path.join(basedir, '/logs')):
    os.mkdir(os.path.join(basedir, '/logs'))

# Настройка логирования
logger = logging.getLogger('START')
logger.setLevel(logging.INFO)

# Формат для логов
log_format = '%(asctime)s | %(levelname).1s | {0:<6} | %(message)s'.format('%(name)s')
formatter = logging.Formatter(log_format, datefmt='%d.%m.%y %H:%M:%S')

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Файловые обработчики для разных типов логирования
log_files = {
    "flask": "logs/flask.log",
    "llm": "logs/llm.log",
    "db": "logs/db.log",
    "faiss": "logs/faiss.log"
}

for name, filename in log_files.items():
    try:
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        file_handler.set_name(name.upper())
        logger.addHandler(file_handler)
    except Exception as e:
        logger.error(f"Ошибка при создании обработчика для {filename}: {e}")


logger.info("Приложение успешно запущено.")
