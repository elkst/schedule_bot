from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для моделей
Base = declarative_base()


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


class Schedule(Base):
    """
    Модель расписания для групп.
    """
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    day = Column(String, nullable=False)  # День недели
    time = Column(String, nullable=False)  # Время занятия
    subject = Column(String, nullable=False)  # Название предмета

    # Связь с группой
    group = relationship("Group", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule(id={self.id}, group_id={self.group_id}, day={self.day}, time={self.time}, subject={self.subject})>"


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
