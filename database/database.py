from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config_data.config import load_config

# Получение конфига и создание движка
db_config = load_config().db
engine = create_async_engine(
    url=f'sqlite+aiosqlite:///{db_config.name}',
    echo=db_config.echo,
)

# Создание фабрики сессий
session_factory = async_sessionmaker(engine)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Создание таблиц в БД в начале работы приложения
async def create_tables() -> None:
    async with engine.begin() as conn:
        from .methods import Users, Schedule, User_settings
        await conn.run_sync(Base.metadata.create_all)
