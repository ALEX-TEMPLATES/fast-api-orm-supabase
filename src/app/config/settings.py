from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Определяем базовую директорию проекта
# Это на 4 уровня выше, чем текущий файл (src/app/config/settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


# Класс настроек приложения
class Settings(BaseSettings):
    # Строка подключения к БД для psycopg3
    DATABASE_URL: str = "..."
    SUPABASE_PROJECT_NAME: str = "..."
    SUPABASE_DATABASE_PASSWORD: str = "..."
    SUPABASE_URL: str = "..."
    SUPABASE_ANON_PABLIC_KEY: str = "..."
    SUPABASE_SERVICE_ROLE_KEY: str = "..."
    USER1EMAIL: str = "..."
    USER1PASSWORD: str = "..."
    USER2EMAIL: str = "..."
    USER2PASSWORD: str = "..."

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


# Экземпляр настроек
settings = Settings()
