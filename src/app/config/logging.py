import logging


class CustomFormatter(logging.Formatter):  # type: ignore
    """Кастомный форматер для логов с голубым цветом уровня."""

    CYAN = "\x1b[36m"
    RESET = "\x1b[0m"

    def format(self, record):
        log_format = (
            f"{self.CYAN}{record.levelname}{self.RESET}:     %(name)s - %(message)s"
        )
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


def setup_logging():
    """Настраивает корневой логгер для использования кастомного форматера."""
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())

    root_logger = logging.getLogger()
    # Очищаем существующих обработчиков, чтобы избежать дублирования логов
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
