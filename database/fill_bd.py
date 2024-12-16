import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Group, Schedule

# Конфигурация базы данных
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Создаем движок и фабрику сессий
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """
    Инициализация базы данных: создание таблиц.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def fill_database():
    """
    Заполнение базы данных тестовыми данными.
    """
    async with async_session() as session:
        # Пример групп
        groups = [
            Group(name="Group 101"),
            Group(name="Group 102"),
            Group(name="Group 103"),
        ]

        # Добавляем группы
        session.add_all(groups)
        await session.flush()  # Генерируем id для групп

        # Пример расписаний
        schedules = [
            Schedule(group_id=groups[0].id, day="Monday", time="09:00", subject="Math"),
            Schedule(group_id=groups[0].id, day="Tuesday", time="11:00", subject="Physics"),
            Schedule(group_id=groups[1].id, day="Monday", time="10:00", subject="Chemistry"),
            Schedule(group_id=groups[1].id, day="Wednesday", time="14:00", subject="History"),
            Schedule(group_id=groups[2].id, day="Friday", time="16:00", subject="Programming"),
        ]

        # Добавляем расписания
        session.add_all(schedules)

        # Сохраняем изменения в базе данных
        await session.commit()

