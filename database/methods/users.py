from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from database.models import User


async def create_user(session: AsyncSession, telegram_id: int, first_name: str, last_name: str, username: str,
                      language_code: str):
    new_user = User(telegram_id=telegram_id, first_name=first_name, last_name=last_name, username=username,
                    language_code=language_code)
    session.add(new_user)
    await session.commit()
    return new_user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int):
    async with session.begin():
        result = await session.execute(select(User).filter_by(telegram_id=telegram_id))
        user = result.scalars().first()
        if not user:
            raise NoResultFound(f"User with telegram_id {telegram_id} not found")
        return user


async def update_user(session: AsyncSession, telegram_id: int, **kwargs):
    user = await get_user_by_telegram_id(session, telegram_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, telegram_id: int):
    user = await get_user_by_telegram_id(session, telegram_id)
    await session.delete(user)
    await session.commit()
