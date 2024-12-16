from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


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