from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from database.database import async_session
from models.groups import Group


class User(Base):
    """
    Модель пользователя.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя
    full_name = Column(String, nullable=False)  # Полное имя пользователя
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="SET NULL"), nullable=True)  # ID группы, если есть

    # Связь с группой
    group = relationship("Group", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, full_name={self.full_name}, group_id={self.group_id})>"

async def add_user(telegram_id: int, full_name: str, group_name: str = None):
    """
    Добавить пользователя в базу данных.
    :param telegram_id: Telegram ID пользователя
    :param full_name: Полное имя пользователя
    :param group_name: Имя группы (опционально)
    """
    async with async_session() as session:
        try:
            # Поиск группы, если указано имя группы
            group = None
            if group_name:
                result = await session.execute(select(Group).where(Group.name == group_name))
                group = result.scalar_one_or_none()
                if not group:
                    print(f"Группа '{group_name}' не найдена.")
                    return

            # Создаем нового пользователя
            user = User(telegram_id=telegram_id, full_name=full_name, group_id=group.id if group else None)
            session.add(user)
            await session.commit()
            print(f"Пользователь '{full_name}' успешно добавлен.")
        except IntegrityError:
            await session.rollback()
            print(f"Ошибка: Пользователь с Telegram ID {telegram_id} уже существует.")
