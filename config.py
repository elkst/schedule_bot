import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    # Токен бота (можно получить у BotFather)
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # ID администратора (для админ панелей и управления)
    ADMIN_ID = int(os.getenv("ADMIN_ID"))

    # URL базы данных для SQLAlchemy
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")

    # Настройки для логирования и отладки
    DEBUG = os.getenv("DEBUG", "True") == "True"
