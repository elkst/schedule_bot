from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Schedule


async def create_schedule(session: AsyncSession, user_id: int, event_name: str, start_time, end_time, description=None,
                          location=None):
    new_schedule = Schedule(user_id=user_id, event_name=event_name, start_time=start_time, end_time=end_time,
                            description=description, location=location)
    session.add(new_schedule)
    await session.commit()
    return new_schedule


async def get_schedule_by_user(session: AsyncSession, user_id: int):
    async with session.begin():
        result = await session.execute(select(Schedule).filter_by(user_id=user_id))
        return result.scalars().all()


async def update_schedule(session: AsyncSession, schedule_id: int, **kwargs):
    async with session.begin():
        schedule = await session.execute(select(Schedule).filter_by(id=schedule_id))
        schedule = schedule.scalars().first()
        if not schedule:
            return None
        for key, value in kwargs.items():
            setattr(schedule, key, value)
        await session.commit()
        return schedule


async def delete_schedule(session: AsyncSession, schedule_id: int):
    schedule = await get_schedule_by_user(session, schedule_id)
    await session.delete(schedule)
    await session.commit()
