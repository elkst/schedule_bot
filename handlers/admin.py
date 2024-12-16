from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from database import async_session
from database import Group
from states.user_states import UserStates
from config import Config  # Импортируем конфиг для доступа к ADMIN_ID

router = Router()


# === Хэндлер вызова панели администратора === #
@router.message(Command("admin"))
async def admin_panel(message: types.Message, state: FSMContext):
    """
    Вызов панели администратора. Доступ только для администраторов.
    """
    # Проверка ID пользователя
    if message.from_user.id != int(Config.ADMIN_ID):
        await message.reply("У вас нет прав администратора.")
        return

    # Создание меню администратора
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить группу", callback_data="admin_add_group")],
        [InlineKeyboardButton(text="Удалить группу", callback_data="admin_delete_group")],
        [InlineKeyboardButton(text="Просмотреть группы", callback_data="admin_view_groups")]
    ])
    await message.answer("Добро пожаловать в панель администратора:", reply_markup=keyboard)


# === Хэндлер для добавления новой группы === #
@router.callback_query(lambda c: c.data == "admin_add_group")
async def add_group(callback_query: CallbackQuery, state: FSMContext):
    """
    Начало процесса добавления новой группы.
    """
    await callback_query.message.answer("Введите название новой группы:")
    await state.set_state(UserStates.adding_group)


@router.message(UserStates.adding_group)
async def save_group(message: types.Message, state: FSMContext):
    """
    Сохранение новой группы в базу данных.
    """
    group_name = message.text.strip()
    if not group_name:
        await message.answer("Название группы не может быть пустым. Попробуйте снова.")
        return

    async with async_session() as session:
        # Проверка на существование группы
        existing_group = await session.execute(select(Group).where(Group.name == group_name))
        if existing_group.scalars().first():
            await message.answer("Группа с таким названием уже существует.")
        else:
            new_group = Group(name=group_name)
            session.add(new_group)
            await session.commit()
            await message.answer(f"Группа '{group_name}' успешно добавлена.")

    await state.clear()


# === Хэндлер для удаления группы === #
@router.callback_query(lambda c: c.data == "admin_delete_group")
async def delete_group_start(callback_query: CallbackQuery):
    """
    Начало процесса удаления группы: отображение всех групп.
    """
    async with async_session() as session:
        result = await session.execute(select(Group))
        groups = result.scalars().all()

    if not groups:
        await callback_query.message.answer("Нет доступных групп для удаления.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=group.name, callback_data=f"delete_group_{group.id}")]
            for group in groups
        ]
    )
    await callback_query.message.answer("Выберите группу для удаления:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("delete_group_"))
async def delete_group(callback_query: CallbackQuery):
    """
    Удаление выбранной группы.
    """
    group_id = int(callback_query.data.split("_")[2])
    async with async_session() as session:
        group = await session.get(Group, group_id)
        if not group:
            await callback_query.message.answer("Группа не найдена или уже была удалена.")
            return

        await session.delete(group)
        await session.commit()
        await callback_query.message.answer(f"Группа '{group.name}' успешно удалена.")


# === Хэндлер для просмотра всех групп === #
@router.callback_query(lambda c: c.data == "admin_view_groups")
async def view_groups(callback_query: CallbackQuery):
    """
    Просмотр всех существующих групп.
    """
    async with async_session() as session:
        result = await session.execute(select(Group))
        groups = result.scalars().all()

    if not groups:
        await callback_query.message.answer("Список групп пуст.")
        return

    groups_text = "\n".join([f"- {group.name}" for group in groups])
    await callback_query.message.answer(f"Список групп:\n{groups_text}")


# === Регистрация хэндлеров === #
def register_handlers(dp: Router):
    dp.include_router(router)
