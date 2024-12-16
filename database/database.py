from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base

# URL для подключения к базе данных SQLite
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Создание движка для асинхронного взаимодействия
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий для работы с базой данных
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функция инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        # Генерация таблиц в базе данных на основе моделей
        await conn.run_sync(Base.metadata.create_all)
