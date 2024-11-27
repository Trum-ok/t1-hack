import os
import logging
from dotenv import load_dotenv

# Загружаем .env файл
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), override=True)

log_dir = os.path.join(basedir, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

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

all_logs_handler = logging.FileHandler(os.path.join(log_dir, 'all.log'))
all_logs_handler.setLevel(logging.INFO)
all_logs_handler.setFormatter(formatter)
logger.addHandler(all_logs_handler)

# Файловые обработчики для разных типов логирования
log_files = {
    "flask": os.path.join(log_dir, "flask.log"),
    "llm": os.path.join(log_dir, "llm.log"),
    "db": os.path.join(log_dir, "db.log"),
    "faiss": os.path.join(log_dir, "faiss.log")
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
        exit(-1)

logger.info("Логирование запущено.")
