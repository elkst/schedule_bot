from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserSetting


async def create_setting(session: AsyncSession, user_id: int, setting_name: str, setting_value: str):
    new_setting = UserSetting(user_id=user_id, setting_name=setting_name, setting_value=setting_value)
    session.add(new_setting)
    await session.commit()
    return new_setting


async def get_settings_by_user(session: AsyncSession, user_id: int):
    async with session.begin():
        result = await session.execute(select(UserSetting).filter_by(user_id=user_id))
        return result.scalars().all()


async def update_setting(session: AsyncSession, user_id: int, setting_name: str, setting_value: str):
    async with session.begin():
        setting = await session.execute(select(UserSetting).filter_by(user_id=user_id, setting_name=setting_name))
        setting = setting.scalars().first()
        if setting:
            setting.setting_value = setting_value
            await session.commit()
        return setting


async def delete_setting(session: AsyncSession, user_id: int, setting_name: str):
    async with session.begin():
        setting = await session.execute(select(UserSetting).filter_by(user_id=user_id, setting_name=setting_name))
        setting = setting.scalars().first()
        if setting:
            await session.delete(setting)
            await session.commit()
