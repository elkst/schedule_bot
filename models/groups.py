from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm import relationship

from models.schedules import Schedule


class Group(Base):
    """
    Модель группы студентов.
    """
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Связь с расписанием
    schedules = relationship("Schedule", back_populates="group", cascade="all, delete-orphan")

    # Связь с пользователями
    users = relationship("User", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"


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