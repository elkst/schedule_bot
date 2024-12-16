from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.exc import NoResultFound

from database.models import Group, User, GroupMember


# Создание группы
async def create_group(session: AsyncSession, name: str):
    new_group = Group(name=name)
    session.add(new_group)
    await session.commit()
    return new_group


# Получение группы по имени
async def get_group_by_name(session: AsyncSession, name: str):
    async with session.begin():
        result = await session.execute(select(Group).filter_by(name=name))
        group = result.scalars().first()
        if not group:
            raise NoResultFound(f"Group with name {name} not found")
        return group


# Добавление участника в группу
async def add_user_to_group(session: AsyncSession, user_id: int, group_id: int, role: str = "member"):
    user = await session.execute(select(User).filter_by(id=user_id))
    user = user.scalars().first()
    group = await session.execute(select(Group).filter_by(id=group_id))
    group = group.scalars().first()

    if not user or not group:
        raise NoResultFound("User or group not found")

    group_member = GroupMember(user_id=user.id, group_id=group.id, role=role)
    session.add(group_member)
    await session.commit()
    return group_member


# Получение всех участников группы
async def get_group_members(session: AsyncSession, group_id: int):
    async with session.begin():
        result = await session.execute(select(GroupMember).filter_by(group_id=group_id))
        return result.scalars().all()


# Удаление участника из группы
async def remove_user_from_group(session: AsyncSession, user_id: int, group_id: int):
    async with session.begin():
        member = await session.execute(select(GroupMember).filter_by(user_id=user_id, group_id=group_id))
        member = member.scalars().first()
        if not member:
            raise NoResultFound("User not in the group")
        await session.delete(member)
        await session.commit()
