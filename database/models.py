from typing import Annotated
from datetime import datetime
from sqlalchemy import String, ForeignKey, Column, Integer, BigInteger, TIMESTAMP, Text
from sqlalchemy.orm import mapped_column, relationship
from .database import Base

# Шаблон для поля первичного ключа
pk = Annotated[int, mapped_column(primary_key=True)]


# Таблица пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    language_code = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с таблицей расписания (один ко многим)
    schedule = relationship('Schedule', back_populates='user')


# Таблица расписания
class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_name = Column(String, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    description = Column(Text)
    location = Column(String)

    # Связь с таблицей пользователей
    user = relationship('User', back_populates='schedule')

    # Связь с таблицей уведомлений (один ко многим)
    notifications = relationship('Notification', back_populates='schedule')


# Таблица настроек пользователя
class UserSetting(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    setting_name = Column(String, nullable=False)
    setting_value = Column(String, nullable=False)

    # Связь с таблицей пользователей
    user = relationship('User')
