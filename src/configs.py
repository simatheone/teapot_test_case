import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'


def configure_logging():
    """
    Устанавливает конфигурации для логера.
    Создает:
        - создает директорию для логов и .log файл.
    Устанавливает:
        - настройки rotating handler;
        - формат логов (дата, формат, уровень, хэндлеры).
    """
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'main_logs.log'

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(datefmt=LOG_DT_FORMAT,
                        format=LOG_FORMAT,
                        level=logging.INFO,
                        handlers=(rotating_handler,))
