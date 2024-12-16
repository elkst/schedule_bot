from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


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